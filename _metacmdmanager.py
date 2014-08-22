################################################################################
# _metacmdmanager.py
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
################################################################################

# Imports.
from Products.PythonScripts import PythonScript
import copy
import string
import urllib
# Product Imports.
import _globals
import _objattrs


################################################################################
################################################################################
###
###   class MetacmdObject
###
################################################################################
################################################################################
class MetacmdObject:

    ############################################################################
    #  MetacmdObject.manage_executeMetacmd:
    #
    #  Execute Meta-Command.
    ############################################################################
    def manage_executeMetacmd(self, custom, lang, REQUEST, RESPONSE):
      """ MetacmdObject.manage_executeMetacmd """
      message = ''
      target = self
      
      # Execute.
      # --------
      for metaCmd in self.getMetaCmds():
        if metaCmd['name'] == custom:
          # Acquire from parent.
          if metaCmd.get('acquired',0) == 1:
            src = getattr(metaCmd['home'],metaCmd['id'])
            ob = getattr(self,metaCmd['id'])
            if ob.meta_type in [ 'DTML Method', 'DTML Document']:
              newData = src.raw
              ob.manage_edit(title=ob.title,data=newData)
            elif ob.meta_type in [ 'Page Template']:
              newData = src.read()
              newContentType = src.content_type
              ob.pt_edit(newData,content_type=newContentType)
            elif ob.meta_type in [ 'Script (Python)']:
              newData = src.read()
              ob.ZPythonScript_setTitle( ob.title)
              ob.write(newData)
          # Execute directly.
          if metaCmd.get('exec',0) == 1:
            ob = getattr(self,metaCmd['id'],None)
            if ob.meta_type in ['DTML Method','DTML Document']:
              value = ob(self,REQUEST,RESPONSE)
            elif ob.meta_type == 'Page Template':
              value = ob()
            elif ob.meta_type == 'Script (Python)':
              value = ob()
            if type(value) is str:
              message = value
            elif type(value) is tuple:
              target = value[0]
              message = value[1]
          # Execute redirect.
          else:
            params = {'lang':REQUEST.get('lang'),'id_prefix':REQUEST.get('id_prefix'),'ids':REQUEST.get('ids',[])}
            return RESPONSE.redirect(self.url_append_params(metaCmd['id'],params,sep='&'))
      
      # Return with message.
      message = urllib.quote(message)
      return RESPONSE.redirect('%s/manage_main?lang=%s&manage_tabs_message=%s'%(target.absolute_url(),lang,message))

################################################################################
