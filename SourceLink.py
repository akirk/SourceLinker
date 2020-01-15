import os
import re
import webbrowser
import sublime
import sublime_plugin
import subprocess

class SourcelinkerCommand( sublime_plugin.TextCommand ):
    def getoutput( self, command ):
        out, err = subprocess.Popen( command, stdout=subprocess.PIPE, shell=True ).communicate()
        return out.decode().strip()

    def run( self, edit, **args ):
        path, filename = os.path.split( self.view.file_name() )
        os.chdir( path + "/" )
        print(path)

        relative_path = path
        for directory in self.view.window().folders():
            relative_path = relative_path.replace( directory, "", 1 )
        relative_path = relative_path.replace( "\\", "/" ).strip( "/" ) + "/"

        # Fallback URL is Github
        remote_url = self.view.settings().get( 'sourcelinker_remote_url', 'https://github.com/{user}/{repo}/blob/{git_rev}/{path}{filename}#L{line}' )
        data = {
            'user': '',
            'repo': '',
            'git_rev': '',
            'path': relative_path,
            'filename': filename,
            'line':''
        }
        git_status = self.getoutput( "git status" )

        if git_status == '':
            if remote_url.startswith( 'https://git' ):
                sublime.status_message( 'SourceLinker: No git repo found' )
                return
        else:
            git_config_path = self.getoutput( "git remote show origin -n" )
            if git_config_path:
                p = re.compile( r"( .+:  )*( [\w\d\.]+ )[:|@]/?/?( .* )" )
                parts = p.findall( git_config_path )
                git_config = parts[0][2]
                if ':' in git_config:
                    data['domain'], data['user'], data['repo'] = git_config.replace( ".git", "" ).replace( ":", "/" ).split( "/" )

                data['path'] = self.getoutput( "git rev-parse --show-prefix" )

                rev_type = self.view.settings().get( 'sourcelinker_revision_type', 'branch' )
               
                if rev_type == 'branch':
                    data['git_rev'] = self.getoutput( "git rev-parse --abbrev-ref HEAD" )
                elif rev_type == 'commithash':
                    data['git_rev'] = self.getoutput( "git rev-parse HEAD" )

        region = self.view.sel()[0]
        first_line = self.view.rowcol( region.begin() )[0] + 1
        last_line = self.view.rowcol( region.end() )[0] + 1
        if first_line == last_line:
            data['line'] = str( first_line )
        else:
            # For now this is hardcoded Github line syntax
            data['line'] = str( first_line ) + "-L" + str( last_line )

        url = remote_url.format( **data )
        webbrowser.open_new_tab( url )
