#!/bin/bash

# build template
xgettext --files-from=movies/i18n/POTFILES.in --directory=./ --output=movies/i18n/locales/template/LC_MESSAGES/messages.pot
# backup old translation file
cp movies/i18n/locales/en/LC_MESSAGES/messages.pot movies/i18n/locales/en/LC_MESSAGES/messages.pot.bak
# create english translation file
cp movies/i18n/locales/template/LC_MESSAGES/messages.pot movies/i18n/locales/en/LC_MESSAGES/messages.pot 
# edit it
vim movies/i18n/locales/en/LC_MESSAGES/messages.pot
# create the .po file out of the .pot file
msgmerge --update --no-fuzzy-matching --backup=off movies/i18n/locales/en/LC_MESSAGES/messages.po movies/i18n/locales/en/LC_MESSAGES/messages.pot
# create the .mo file out of the .po file
msgfmt movies/i18n/locales/en/LC_MESSAGES/messages.po --output-file movies/i18n/locales/en/LC_MESSAGES/messages.mo

exit 0
