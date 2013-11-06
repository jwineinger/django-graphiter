graphiter
=========

Simple Django app to store graphite chart URLs, combine them into pages, and adjust time frames via GET param.

To use:   
1) install the `graphiter` app to your python path.  
2) Add `graphiter` to your INSTALLED_APPS  

    INSTALLED_APPS = [
      ...
      'graphiter',
      ...
    ]

3) Include the `graphiter.urls` from your projects urlconf  
    
    url(r'^', include('graphiter.urls')),
