from flask import url_for, current_app, redirect, request
from rauth import OAuth2Service

import json
import urllib2


class OAuthSignIn(object):
    """
    Generic Parent OAuthSignIn class
    """
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = current_app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials['id']
        self.consumer_secret = credentials['secret']

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('.oauth_callback',
                       provider=self.provider_name, _external=True)

    @classmethod
    def get_provider(self, provider_name):
        if self.providers is None:
            self.providers = {}
            for provider_class in self.__subclasses__():
                provider = provider_class()
                self.providers[provider.provider_name] = provider
        return self.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    """
    A Google signin subclass of OAuthSignIn
    """

    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        """
        This will pull the most up to date google auth urls from
        Google's published list of information
        """
        googleinfo = urllib2.urlopen('https://accounts.google.com/'
                                     '.well-known/openid-configuration')
        google_params = json.load(googleinfo)
        self.service = OAuth2Service(
            name='google',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url=google_params.get('authorization_endpoint'),
            base_url=google_params.get('userinfo_endpoint'),
            access_token_url=google_params.get('token_endpoint')
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        """
        the class returns the data I am interested in for the user profile
        """
        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            },
            decoder=json.loads
        )
        me = oauth_session.get('').json()
        return(me['name'],
               me['email'])

"""
A Facebook signin subclass of OAuthSignIn
"""


class FacebookSignIn(OAuthSignIn):
    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        """ Initialize the Facebook service """
        self.service = OAuth2Service(
            name='facebook',
            client_id=self.consumer_id,
            client_secret=self.consumer_secret,
            authorize_url='https://www.facebook.com/dialog/oauth',
            base_url='https://graph.facebook.com/',
            access_token_url='/oauth/access_token'
        )

    def authorize(self):
        return redirect(self.service.get_authorize_url(
            scope='email',
            response_type='code',
            redirect_uri=self.get_callback_url())
        )

    def callback(self):
        """
        the class returns the data I am interested in for the user profile
        """
        if 'code' not in request.args:
            return None, None, None

        oauth_session = self.service.get_auth_session(
            data={
                'code': request.args['code'],
                'grant_type': 'authorization_code',
                'redirect_uri': self.get_callback_url()
            }
        )

        me = oauth_session.get('me').json()
        # import pdb
        # pdb.set_trace()
        print me
        return (
            me['name'],
            'facebook' + me['id'] + '@noemail.com'
        )
