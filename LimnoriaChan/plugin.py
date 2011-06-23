###
# Copyright (c) 2011, Valentin Lorentz
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

import re

import supybot.utils as utils
import supybot.world as world
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
from supybot.i18n import PluginInternationalization, internationalizeDocstring

_ = PluginInternationalization('LimnoriaChan')

WEB_REPO = 'https://github.com/ProgVal/Limnoria'
PLUGINS_WEB_REPO = 'https://github.com/ProgVal/Supybot-plugins'
staticFactoids = {
        'git':          WEB_REPO,
        'git-pl':       PLUGINS_WEB_REPO,
        'wiki':         WEB_REPO + '/wiki',
        'issues':       WEB_REPO + '/issues',
        'issues-pl':    PLUGINS_WEB_REPO + '/issues',
        'supybook':     'http://supybook.fealdia.org/',
        }
dynamicFactoids = {
        'git':          WEB_REPO + '/tree/%s',
        'git-pl':       PLUGINS_WEB_REPO + '/tree/%s',
        'file':         WEB_REPO + '/blob/%s',
        'file-pl':      PLUGINS_WEB_REPO + '/blob/%s',
        'commit':       WEB_REPO + '/commit/%s',
        'commit-pl':    PLUGINS_WEB_REPO + '/commit/%s',
        'wiki':         WEB_REPO + '/wiki/%s',
        'issue':        WEB_REPO + '/issues/%s',
        'issue-pl':     PLUGINS_WEB_REPO + '/issues/%s',
        }

@internationalizeDocstring
class LimnoriaChan(callbacks.Plugin):
    """Add the help for "@plugin help LimnoriaChan" here
    This should describe *how* to use this plugin."""

    _addressed = re.compile('^([^ :]+):')
    _factoid = re.compile('%%([^ ]+)')
    _dynamicFactoid = re.compile('^(?P<name>[^#]+)#(?P<arg>.*)$')
    def doPrivmsg(self, irc, msg):
        if not world.testing and \
                msg.args[0] not in ('#limnoria', '#limnoria-bots'):
            return
        if callbacks.addressed(irc.nick, msg):
            return

        # Internal
        match = self._addressed.match(msg.args[1])
        if match is None:
            prefix = ''
        else:
            prefix = match.group(1) + ': '
        def reply(string):
            irc.reply(prefix + string, prefixNick=False)

        # Factoids
        matches = self._factoid.findall(msg.args[1])
        for name in matches:
            arg = None
            match = self._dynamicFactoid.match(name)
            if match is not None:
                name = match.group('name')
                arg = match.group('arg')
            name = name.lower()
            if arg is None:
                if name in staticFactoids:
                    reply(staticFactoids[name])
            else:
                if name in dynamicFactoids:
                    reply(dynamicFactoids[name] % arg)

Class = LimnoriaChan


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
