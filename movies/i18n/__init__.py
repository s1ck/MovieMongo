# -*- coding: utf-8 -*-

import gettext

path = 'movies/i18n/locales'
domain = 'messages'
languages = ['en']
translation = gettext.translation(domain, path, languages)
translation.install()
