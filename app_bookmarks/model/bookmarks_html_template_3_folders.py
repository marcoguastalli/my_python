class BookmarksHtmlTemplate:

    def __init__(self):
        self.template = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<META HTTP-EQUIV="Content-Type" CONTENT="text/html; charset=UTF-8">
<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'none'; img-src data: *; object-src 'none'"></meta>
<TITLE>Bookmarks</TITLE>
<H1>Bookmarks Menu</H1>
<DL><p>
    <DT><H3>MENU FOLDER 1</H3>
    <DL><p>
        <DT><H3>TOOLBAR FOLDER 1 SUB FOLDER</H3>
        <DL><p>
            <DT><A HREF="http://127.0.0.1/">MENU FOLDER 1 SUB FOLDER LINK</A>
        </DL><p>
        <DT><A HREF="http://127.0.0.1/">TOOLBAR FOLDER 1 LINK 1</A>
    </DL><p>
    <DT><A HREF="http://127.0.0.1/">MENU LINK 1</A>
    <DT><H3 PERSONAL_TOOLBAR_FOLDER="true">Bookmarks Toolbar</H3>
    <DL><p>
        <DT><H3>TOOLBAR FOLDER 1</H3>
        <DL><p>
            <DT><H3>TOOLBAR FOLDER 1 SUB FOLDER</H3>
            <DL><p>
                <DT><A HREF="http://127.0.0.1/">TOOLBAR FOLDER 1 SUB FOLDER LINK</A>
            </DL><p>
            <DT><A HREF="http://127.0.0.1/">TOOLBAR FOLDER 1 LINK 1</A>
        </DL><p>
        <DT><A HREF="http://127.0.0.1/">TOOLBAR LINK 1</A>
    </DL><p>
    <DT><H3 ADD_DATE="1681216735">Other Bookmarks</H3>
    <DL><p>
        <DT><H3>OTHERS</H3>
        <DL><p>
            <DT><H3>OTHERS FOLDER 1 SUB FOLDER</H3>
            <DL><p>
                <DT><A HREF="http://127.0.0.1/">OTHERS FOLDER 1 SUB FOLDER LINK</A>
            </DL><p>
        </DL><p>
        <DT><A HREF="http://127.0.0.1/">OTHERS LINK 1</A>
    </DL><p>
</DL>
"""
