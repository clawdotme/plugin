#!/usr/bin/env python3
"""Owner-approved Claw Me authorization. Secrets are stored locally, never printed."""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qs, urlsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

ORIGIN = 'https://claw.me'

class AuthorizationError(Exception):
    pass

class HTTPRejection(AuthorizationError):
    def __init__(self, code):
        self.code = code
        super().__init__('http_' + str(code))

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise AuthorizationError('redirect_refused')

def post(path, body):
    try:
        request = Request(ORIGIN + '/api/v1/agent-auth' + path,
                          data=json.dumps(body).encode(),
                          headers={'Content-Type': 'application/json'}, method='POST')
        with build_opener(NoRedirect()).open(request, timeout=30) as response:
            return json.load(response)
    except HTTPError as error:
        raise HTTPRejection(error.code) from None
    except (URLError, OSError, ValueError):
        raise AuthorizationError('request_failed; state retained; do not create a duplicate') from None

def save(path, data):
    fd, temporary = tempfile.mkstemp(prefix='.authorization-', dir=path.parent)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, 'w') as file:
            json.dump(data, file)
            file.flush()
            os.fsync(file.fileno())
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)

def load(path):
    if not path.exists():
        return None
    if path.is_symlink() or not stat.S_ISREG(path.stat().st_mode):
        raise AuthorizationError('unsafe_state_file')
    if path.stat().st_mode & 0o077 or path.stat().st_uid != os.getuid():
        raise AuthorizationError('state_file_must_be_owned_by_you_and_mode_0600')
    try:
        return json.loads(path.read_text())
    except (ValueError, OSError):
        raise AuthorizationError('invalid_state_file') from None

def public(state, path):
    result = {'status': state['status'], 'state_file': str(path), 'scopes': state['scopes']}
    if state['status'] == 'pending':
        uri = urlsplit(state.get('verification_uri', ''))
        if (uri.scheme != 'https' or uri.netloc != 'claw.me'
                or not state.get('user_code')
                or parse_qs(uri.query, keep_blank_values=True).get('code') != [state['user_code']]):
            raise AuthorizationError('invalid_verification_origin')
        for key in ('verification_uri', 'user_code', 'expires_at'):
            result[key] = state[key]
    return result

def run(args):
    path = Path(args.state).expanduser().absolute()
    # Reject symlink components rather than silently writing through them.
    for part in (path, *path.parents):
        if part.is_symlink():
            raise AuthorizationError('symlink_state_path_refused')
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    lock = path.with_name(path.name + '.lock')
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError:
        raise AuthorizationError('state_busy; inspect existing operation before retrying') from None
    os.close(fd)
    try:
        state = load(path)
        if args.command == 'start':
            scopes = list(dict.fromkeys(args.scope))
            if not scopes or any(not re.fullmatch(r'[a-z][a-z0-9_-]*:[a-z][a-z0-9_-]*', s) for s in scopes):
                raise AuthorizationError('explicit_valid_scopes_required')
            identity = {'owner_email': args.email, 'client_name': args.client_name,
                        'client_type': args.client_type, 'scopes': scopes}
            if state:
                if state.get('identity') != identity:
                    raise AuthorizationError('state_belongs_to_different_request; use a separate state file')
                if state.get('status') in ('rejected', 'unavailable', 'invalid_response'):
                    raise AuthorizationError('previous_request_' + state['status'] + '; inspect the issue and explicitly choose a new state file to start again')
                if state.get('status') == 'exchanging':
                    raise AuthorizationError('exchange_outcome_unknown; inspect private state; do not retry or create a duplicate')
                if state.get('status') == 'creating':
                    raise AuthorizationError('creation_outcome_unknown; do not automatically create another request')
                return public(state, path)
            state = {'status': 'creating', 'identity': identity, 'scopes': scopes}
            save(path, state)  # Preflight writable storage and prevent duplicate creation after uncertainty.
            try:
                reply = post('/requests', identity)
            except HTTPRejection as error:
                if 400 <= error.code < 500 and error.code != 408:
                    state['status'] = 'rejected'
                    save(path, state)
                    raise AuthorizationError('request_rejected_http_' + str(error.code) + '; correct the request and explicitly choose a new state file') from None
                raise
            state['status'] = 'invalid_response'
            state['private_response'] = reply
            save(path, state)
            for key in ('request_id', 'device_secret', 'verification_uri', 'user_code', 'expires_at'):
                state[key] = reply[key]
            state['status'] = 'invalid_response'
            save(path, state)  # Persist device secret before producing any output.
            uri = urlsplit(state.get('verification_uri', ''))
            if (uri.scheme != 'https' or uri.netloc != 'claw.me'
                or not state.get('user_code')
                or parse_qs(uri.query, keep_blank_values=True).get('code') != [state['user_code']]):
                raise AuthorizationError('invalid_verification_origin')
            if (not isinstance(state.get('request_id'), str) or not re.fullmatch(r'[a-fA-F0-9]{8}-(?:[a-fA-F0-9]{4}-){3}[a-fA-F0-9]{12}', state['request_id'])
                    or not isinstance(state.get('device_secret'), str) or not 30 <= len(state['device_secret']) <= 300
                    or not isinstance(state.get('user_code'), str) or not re.fullmatch(r'[A-Z0-9]{5}-[A-Z0-9]{5}', state['user_code'])):
                raise AuthorizationError('invalid_authorization_response')
            try:
                expiry = datetime.fromisoformat(state['expires_at'].replace('Z', '+00:00'))
                if expiry.tzinfo is None:
                    raise ValueError()
            except (ValueError, TypeError, AttributeError):
                raise AuthorizationError('invalid_authorization_expiry') from None
            state['status'] = 'pending'
            save(path, state)
            return public(state, path)
        if not state:
            raise AuthorizationError('start_required')
        if state.get('status') in ('rejected', 'unavailable', 'invalid_response'):
            raise AuthorizationError('previous_request_' + state['status'] + '; inspect the issue and explicitly choose a new state file to start again')
        if state.get('status') == 'authorized':
            return public(state, path)
        if state.get('status') == 'exchanging':
            raise AuthorizationError('exchange_outcome_unknown; inspect private state; do not retry or create a duplicate')
        if state.get('status') != 'pending' or not re.fullmatch(r'[a-fA-F0-9-]{36}', state.get('request_id', '')):
            raise AuthorizationError('invalid_pending_state')
        state['status'] = 'exchanging'
        save(path, state)  # Token delivery is single-use; uncertain exchange must not be retried.
        try:
            reply = post('/requests/' + state['request_id'] + '/token', {'device_secret': state['device_secret']})
        except HTTPRejection as error:
            if error.code == 429:
                state['status'] = 'pending'
                save(path, state)
                raise AuthorizationError('rate_limited; wait before polling the same state again') from None
            if 400 <= error.code < 500 and error.code != 408:
                state['status'] = 'unavailable'
                save(path, state)
                raise AuthorizationError('authorization_unavailable_http_' + str(error.code) + '; explicitly choose a new state file to request approval again') from None
            raise
        state['private_token_response'] = reply
        save(path, state)  # Preserve single-use token delivery before validating its contents.
        if reply.get('status') == 'authorization_pending':
            state['status'] = 'pending'
            save(path, state)
            return public(state, path)  # Exactly one poll; caller may retry after owner approval.
        if reply.get('status') != 'authorized' or not isinstance(reply.get('api_key'), str) or not reply['api_key']:
            raise AuthorizationError('invalid_token_response')
        approved = reply.get('scopes')
        if not isinstance(approved, list) or any(scope not in state['identity']['scopes'] for scope in approved):
            raise AuthorizationError('invalid_approved_scopes; exchange state retained')
        state.update(status='authorized', api_key=reply['api_key'], scopes=approved)
        state.pop('device_secret', None)
        state.pop('private_response', None)
        state.pop('private_token_response', None)
        save(path, state)
        return public(state, path)
    finally:
        lock.unlink()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    start = sub.add_parser('start')
    start.add_argument('--email', required=True)
    start.add_argument('--client-name', required=True)
    start.add_argument('--client-type', default='generic')
    start.add_argument('--scope', action='append', required=True)
    for command in (start, sub.add_parser('poll')):
        command.add_argument('--state', required=True, help='Private JSON file; retains credential after approval')
    try:
        print(json.dumps(run(parser.parse_args())))
    except (AuthorizationError, OSError, KeyError, TypeError, ValueError) as error:
        # Only our constant errors are printable; OS/server messages can contain secrets.
        print(json.dumps({'error': str(error) if isinstance(error, AuthorizationError) else 'local_or_response_error; private state retained'}))
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())
