from authomatic.providers import oauth2, oauth1

CONFIG = {
    
    'fb': {
           
        'class_': oauth2.Facebook,
        
        # Facebook is an AuthorizationProvider too.
        'consumer_key': '630259823729024',
        'consumer_secret': 'e196f5e64b6c6f528ad9a2b02d1507de',
        
        # But it is also an OAuth 2.0 provider and it needs scope.
        'scope': ['user_about_me', 'email', 'publish_stream'],
    }, 

    'tw': { # Your internal provider name
        
         # Provider class
         'class_': oauth1.Twitter,
        
         # Twitter is an AuthorizationProvider so we need to set several other properties too:
         'consumer_key': 'HHtzVZhu3XDhadA3qRih1MJJz',
         'consumer_secret': '8h2oitbipCrncqa6Y3rNbPq2SBgAfiDs3sndvCQMoUflpTSDvn',
     },
    
    
   #  'oi': {
           
   #      # OpenID provider dependent on the python-openid package.
   #      'class_': openid.OpenID,
   #  }
}
