import re

f = """
    alibri" style="FONT-SIZE:11pt"><a href="141/S141497.html">5/14/18 21:00</a></font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">Colorado Springs</font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">CO</font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">Light</font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">20 minutes</font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">My boyfriend and I have seen these several times. We just now found this site and we are amazed. We were driving between fort Carson an</font></td>
<td bgcolor="#FFFFCC"><font color="#000000" face="Calibri" style="FONT-SIZE:11pt">5/15/18</font></td>
    
    """
x = re.sub('<[^>]*>', '', f)  # you can also use re.sub('<[A-Za-z\/][^>]*>', '', f)

print('\n'.join(x.split()))