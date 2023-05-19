
import socket
import ipaddress
from selenium import webdriver

# def ip_Address(request):

#     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
#     if x_forwarded_for:
#         ip = x_forwarded_for.split(',')[0]
#     else:
#         ip = request.META.get('REMOTE_ADDR')
#     # ipaddress.ip_address('192.168.0.1')
#     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#     s.connect(("8.8.8.8", 80))
#     ip_addr = s.getsockname()[0]
#     print("MY IP ADDRESS:",(s.getsockname()[0]))
#     ip = ipaddress.IPv4Address(ip_addr)
#     print("Is global:", ip.is_global)
#     print("Is link-local:", ip.is_link_local)
#     network = ipaddress.IPv4Network(ip_addr)


#     # hostname = socket.getfqdn() 
#     # IPAddr = socket.gethostbyname(hostname)    
#     print("Your Computer Name is:" , network.overlaps(ipaddress.IPv4Network(ip_addr)))   
#     print("Hosts under", str(network), ":")
#     # for host in network.hosts():
#     #     print("sdfsfsdf:",host)
#     for subnet in network.subnets(prefixlen_diff=2):
#         print(subnet) 
#     # print("Your Computer IP Address is:" , IPAddr)
#     return ip


# from webdriver_manager.firefox import GeckoDriverManager

# driver = webdriver.FirefoxProfile(executable_path=GeckoDriverManager().install())    
# def ip_Address(proxy,port):
#     profile = webdriver.Firefox(executable_path=GeckoDriverManager().install())    
#     profile.set_preference("network.proxy.type", 1)
#     profile.set_preference("network.proxy.http", proxy)
#     profile.set_preference("network.proxy.http_port", port)
#     profile.set_preference("network.proxy.ssl", proxy)
#     profile.set_preference("network.proxy.ssl_port", port)
#     driver = webdriver.Firefox(profile)
#     return driver
# PROXY = "11.456.448.110:8080"
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--proxy-server=%s' % PROXY)
# chrome = webdriver.Chrome(chrome_options=chrome_options)
# chrome.get("https://www.google.com")


