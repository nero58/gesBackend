from django_hosts import patterns, host
host_patterns = patterns(
    '',
    host(r'', 'gesBackendApi.urls', name=' '),
    host(r'gesadmin', 'gesBackendApi.admin_url', name='admin')
)