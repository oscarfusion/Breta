PIPELINE_CSS = {
    'base': {
        'source_filenames': (
            'css/vendors/bootstrap.css',
            'css/base.css',
        ),
        'output_filename': 'cache/css/base.css',
    },
}

PIPELINE_JS = {
    'base': {
        'source_filenames': (
            'js/vendors/jquery-1.10.2.js',
            'js/vendors/handlebars-v2.0.0.js',
            'js/vendors/ember-1.9.0.js',
        ),
        'output_filename': 'cache/js/base.js',
    }
}
