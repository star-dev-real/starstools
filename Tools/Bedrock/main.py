import json, os, time, asyncio, threading, winreg, atexit
from mitmproxy import http, options
from mitmproxy.tools.dump import DumpMaster

time_spent = 0
points = 0
lesson = 0
auto_answer = False

def set_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 1)
    winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "127.0.0.1:8082")
    winreg.CloseKey(key)

def disable_proxy():
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
                         0, winreg.KEY_SET_VALUE)
    winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
    winreg.CloseKey(key)

atexit.register(disable_proxy)

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_header():
    print(f"""███████╗████████╗ █████╗ ██████╗     ██████╗ ███████╗██████╗ ██████╗  ██████╗  ██████╗██╗  ██╗
██╔════╝╚══██╔══╝██╔══██╗██╔══██╗    ██╔══██╗██╔════╝██╔══██╗██╔══██╗██╔═══██╗██╔════╝██║ ██╔╝
███████╗   ██║   ███████║██████╔╝    ██████╔╝█████╗  ██║  ██║██████╔╝██║   ██║██║     █████╔╝ 
╚════██║   ██║   ██╔══██║██╔══██╗    ██╔══██╗██╔══╝  ██║  ██║██╔══██╗██║   ██║██║     ██╔═██╗ 
███████║   ██║   ██║  ██║██║  ██║    ██████╔╝███████╗██████╔╝██║  ██║╚██████╔╝╚██████╗██║  ██╗
╚══════╝   ╚═╝   ╚═╝  ╚═╝╚═╝  ╚═╝    ╚═════╝ ╚══════╝╚═════╝ ╚═╝  ╚═╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝
                                                                                            """)
    print()

def print_menu():
    print("[0] Edit Time")
    print("[1] Edit Points")
    print("[2] Edit Lesson")
    print("[3] Auto Answer")
    print("[4] Start Proxy")
    print("[5] Exit")
    print()

def request(flow: http.HTTPFlow):
    types = ['.png', '.jpg', '.jpeg']
    url = flow.request.pretty_url
    if any(url.endswith(ext) for ext in types):
        url = "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxARDw8QEBAPDxAPDg8PDQ0PDw8NDxAPFREWFhURFRUYHSggGBolGxUVITEhJSkrLi4uFx8zODMuNygtLisBCgoKDg0OGhAQFy0fHiUtLS0tLSstLS0tLS0tLS0tLSsrLS0tLS0tLS0tKystKystLS0tLS0tKystLS0tLS0rK//AABEIAOcA2gMBEQACEQEDEQH/xAAcAAABBQEBAQAAAAAAAAAAAAAAAgMEBQYBBwj/xAA/EAACAgADBQUGAggEBwAAAAAAAQIDBAURBhIhMVETIkFhcTKBkaGxwQfhFCNCUnKS0fBiY3OyFSQlQ2SC8f/EABoBAQACAwEAAAAAAAAAAAAAAAABAgMEBQb/xAAyEQEAAgIBAwIFAgYCAgMAAAAAAQIDEQQSITEFQRMiMlFhcaEzQoGRscEj0eHxFBUk/9oADAMBAAIRAxEAPwD3EAAAAAAAAAAAAAAAKXP857FbsNN9+PNR/M5vM50Yvlr5bGLD1d5ZmrF3Sbk52SfVyf8AaODk5+Te+qW10V8aXOXZzOLSm3OPinxkvNPx9Gb3E9VnfTk7ww5MMT4aWuxSSlF6prVNHoa2i0bhqTGu0lEoAAAAAAAAAAAAAAAAAAAAAAAAAAAAAEbH4ns4N+L4R9eprcvkRhxzb39mTHTqtpg8zt37DyFsk2mZl0dahodnsEnS21rq/kTg4N+TFpr/ACtfLk6Zcx2Xaayj4eBpzFsdtSvW+y8lxu5Lck+7J/yy6+jPRel87U/DtPZizY994aI9C1AAAAAAAAAAAAAAAAAAAAAAAAAAAAABm86xe9J6PhHgvuzy3qvJ679MeIdDj49Rtl4Pem35nM8QzWb3I692iHnxPR+iV1gm33tLn55+Y/iK/Exeq8Osx1xCMdmdxlO7J9H9DzeK81ltxO4XeUYvfjut6yilx6x8H9v/AKez4HK+Nj7+YamWmp2nm+xAAAAAAAAAAAAAAAAAAAAAAAAAAAi5jiNytvxfCPr1NXmZvhYpt7+zJip1W0x2YW91ni7267upWNQgYGP1LWY7PQ8FHSuC/wAKPV+k16eJT87n93OyT80nbFwNjl06sUwrXyqMfTqvQ8Pnr0XbdJV2Ftdc01zT5dV4o3eBypxZIla9eqGnqsUoqS4prVHsq2i0RaPDSmNTossgAAAAAAAAAAAAAAAAAAAAAAAAAZ7PMTvT3Vyjw9/j/fkea9X5PVboj2b3GpqNs1mc+SOLjj3bc+D2V1ayiurQyT2YLS31S7q9Ee24denj0j8Q51vMuszZI3WUQhXRPGc7H3ls1lTYqrRnPpbTNEp2T4rR7j5S4x8peK956n0nmbj4dv6MGWnuuTutcAAAAAAAAAAAAAAAAAAAAAAAAxjb9yDl48o+pg5OaMWObL469VtMlbPVtniM+Sb2dWsahTYiW9MmkagtK7yWrvx8uJS3eYhr3ns2KPe441WI/Dny6ybeJEO08pzY7yz1QsVXqjiWjVmWsq/TR6cuj6PqbGDLNLRMLz3X+X4rtI8fajwmvPr7z23E5MZ8fV7+7TvXplKNpQAAAAAAAAAAAAAAAAAAAAAAGfzvFb0t1co8Pf4nm/VuV1W6I8R/lvcbHqNypMVPSLOBHeW2rsNHV6mee0MdpajIqeOvuHHp8TPWv5a+SezSHvGk5LkY8s6pKYRLDy3Kncs1TE0cjLVeEDE1GOJZIkjD4hwkpLmuEo/vR6HV4HMnDf8ACL1iY00NF0ZxUovVP+9D2GPJXJWLV8NOYmJ1JwugAAAAAAAAAAAAAAAAAAABEzHF9nHh7T5eXmaXO5UYMf5nx/2y4sfXP4ZeyWr1Z4zLkm07dOsaVmOt1eiJpUmS8HXyJtLFLY5RRuxXxOl6Lg6805J9mpmssj1jXItZpc3J010tWEWTPNZbblmg3I07xsk1ZDVGraNSvEq66vQtWWSDVeMsqblDin7Vb5Pz8mdXh+oXw+6JpFu0pVe1tPKcZQfj4nap6vSfNf3Uniz7SlV7S4V/t6eqM9fUsM/eGOeNdIhneGf/AHY/MyxzsE/zftKvwL/Y7HMqHyth/MkZI5WGf5oR8K/2PQxNb5Tg/SUWXjLSfFo/urNbR7HTIqAAAAAAAAAAAAhYvMYQXBqT+SOfyvUcWGNRO5ZseG1mWzLNo6tylqzy3Iz3z23Lo48cVjsqp49y5cEYoppMyTWtWWmVJX2T4TeaenBGLU3tFY8yxXtqGrphoj2nA4vwMUV92ja25OG5M6VR7ZHA5ubqsy1gyzk2lkJZilEkMwXqQZur1MHhkiVbfSXiWSJVuJwyfNGSLMkSgzy+JaLyv1yQ8vRb4tvudTiwHmW+Nb7nUXHBvqyf/kWRtMw3aQfdssj6SaM1Odkp4lS0RPmGlyrMrHwse8v3tNJL16nZ4fqvVPTk/u1cmKPZdncawAAAAAbtvhH2pJfUw5M+PH9dohatLW8Qq8ZtBVDxXvf2Obm9XpXtSN/q2KcW0+WbzHa5PVRbl5Lgjk5+fmy+Z7NqnGrVRYjNb7eXdRoz38tiIiDVWGk3rJthWbJ1NJEyxzK5yzLJTa4aLqUjdp6axuWO1ohrcFhFBJaHpfTfTPg/8mT6mlkydSUdtiIskaXMzdFdQtWEaTPOZb7lmgk1pSSysoJZSUOGG1Vok1ZUmYu8LxKFdhSYsvFkWeFLbW6jf6KTtPUVHBjqR1H4YEjqR1Ho4NIjqRuSt5R5GTFaeo6dpEMxkkl0SSPX4uTeKR+kMM4o2ujqNYi26MVrJpepjyZaY43edLVrNvClx209NeqT3n8TmZvVqV7Ujf6tinFtPlQY3a22XCEWl8Dl5vUc1/5tfp2bNeNSvlTX47E2c5aLojRnJMs8RWEb9DlL2m36sps6z9WBXQrtWbp1GXSfKLfois3iFJstcLkFkua0+pfHjy5Z1Ssyx2yxC8weRQjxfF+f9DqYPRct++WdR9oYLcj7LWupR5I73G4WHjx8kf1a9rTPks21SZS0MObNGONpiNo85HnuRmm8ssQbZoWldxmPYSykyhwrMiqzXaLB4WUYYjE00zmtYwnNKbjy3tOaXnyL4+PlyxulZkWFN0ZxjOEozhJKUJxalGUXyaa4NGrbtOp8rFtFdBLrRGk7J7FEJ27uJEbSRKaJWiEe24mIXiqutxOslFcW3ol1Zt8XFN7xEMvTqNy1FOBgoxTWrUUm+rS5nuKYa1rEacu2SZnZrNcxVUX10+Bp87nfA+Wv1f4ZMWLq7z4Y3G4q25vVy06Hm8vItedzO5btYivg1TlU5PhE17ZEzdY07OTfPRfMmtcl/pqxzliE6rZheMvgjax+ncnJ4iIUnkQm07N1Lnq/eb1PQ8k/Xk1+kMc8mfaE2rKaY8oL38Tbp6Hgj6pmWOc9pSoUxXJI3cfp3Gx/TSP8sc3tPucNyKxHaIVBICJnQRKw1M3LrTwtFUeyzm29EubOJn5M2nuyRDynNPxgSvnDCYRYimEt1XzudXa6Pi4RUXpHo3z6Iz19Ntau721P20ncNzsvtHTj8OrqtYtS3Lqp6b9ViSbi+vNNPxT9xyeTivgv0W/9rLds19ocKzY042Y5stEPnLKKZZpmNllm/OWKnZNaNJx1i+yjxT7se4tOkdOHM9xjxRhx1x19u39ff92He+71bYnL78uvtwFr1qnX+lYTpFqSjbFe+UHp13n4nn/XsGunNrv4n/X+/wBmXFO+zab5wIll6Q5k7Okh2EJ6TU7SVoqjW3ExC8VVuMxWiMla7Zq0TNlcE52O6S7sPZ85/l/Q9N6TxdfPPs1uXl1HTDWnfc5j82e/Z3uW++HnqeN515nNbbpUjVOyZhcNHRcEcy1pY5mU+EEuRFPO2OZk/GR0MeWa+JV8lqbNmvKvHujpKVrNinPyR7o6YKVzNmvqV/dHQ72xmj1L8I6He1Lf/Y/hHQ47TFb1G3snoIlYamTmWt5laKkORp3zbW0z232IcMqzCUW1L9DujFrg05QcU0/eV489WekT94TPh5l+DuRRvtt3/ZjS4yXVS4NHqYjqtpintDX5Tlv/AA7Op4eHCjHYV2Vr/Nqlrp/K7Pkcj1nF/wAcW+0/tP8A50vSdw3Op5vqZNONlZlOkbHT/VWf6c/9rFfqhbTxP8HZxhj6d7hrFqPru8D31p/5P6tbXyvaNqFGMsHbyccT2evWNsJQ0/m3X7jR9Zxxfi2/Hf8AsnD9Qdh4qIbuiHaTpOjcrRpOjNlxbS0VQcTidC0Qy1qgYeuV9sYR4tvT8zocPjzkvEQZLxSu3oeCw0aq41x5RXPq/FnssWOMdYrDi3tNp3J8yKsxnuFcZt/sye8n0fiea9V4sxfqj3dDj33GkKnHyhz4rqjg2ozzjifCxozWuXiY+mYYpwymV4iL5MtF5hinHJ1SMsZVOmSlIyRkQ7vF4yDupeMhoak/ENDeKzlNOORjnIEuRjnInTMfiTP/AKTjf9KK+NkUbHBtvk0/UmOzHfg5mEa7ZQlou0hon5pnq6W1fupaN1anbnFxjmGUWJ8YYl1t/wCG1dm/9xr+pR14rR+J/buYoalzPGbbGiHMrtOjOIlrCS6xkvkInvC0Q+dsgxMqp1zi9HHda9x7zN5a2Pw9Ezza2V1WH14bl1Nj9YTT+xr5rTkpNZ+0/wCFq06Z23UrDxem5o27CU6NTtJ0mIRL7y0QyRVU4i9t6Iz48e5ZPENrsnlfZ19rJd+a7vlH8z1np3GjHTrnzLk8rL1W1DQHSagAZxWHjZFxlyfJ9H1MeXFXJXpstW01ncMlmOBlVJprVeD8GjyvM4Vsdu7pYssWhWW4dPjF7rOdMa8tiLG6sbZW9Ja+pWaxKZrErjCZunzZimmmK2JZVY5PxK94YZxpEb0Wiyk0LVhbrlXod3yeuUdIcyOo6SXMrtbpJcyNp6Wb/EPjlWOX+Tr8Jxf2NvgT/wDpp+qL1+V43kOKlW4zi9HFnq8nlSveF9nucStlTNvV1TrmvVST+xindomJ+y3Tp7F2p4tn6SJWkJ0ZnaTpaIeAV1bts4/uzlH4SaPdzPVWJ/DSr2nSztg+zfozDHllnw9crt1jF9Un8jx0xqW3EOSsCdI9txMQvEK3FXmStWSIWOy2V9tbvSXchxl5+R2vTuL127+Gnys3TGoehJHp3JdAAABrEURsi4yWq+a80Y8mKuSvTaFq2ms7hlM0yqVT1XGL5SX98zzfM4Nsc78w6GLNFlZLR8JI5VqTDZiUO/COPGD4dCv6rxYirHSjwZE0WmsSscPmnmY5oxzjWNOY6lJqxzjS68WmV7qTQ6rhtHSO0I2dJLsG09Kn2tjv5fjYLnLCX7q81W2vmjY4ltZ6TP3j/KL1+WXieUR1PZZGrj8LLGU6Vt+Rir5ZbeHsVN3cj/DH6HjbR80tqIdlaV0nRmdpMQnTxzMatzHYmP8A5FrXpKTkvkz2nHt1cek/iP8Apz7RrJMflaW1fqpP/C/oUj6mSfD0KqfdiukUvkeSt5lvRDk7CFohEvsLRC0Qhwg5zSXizaw06pRedQ9NyXAKimMNO81rP16HsOLh+FjiPf3cTNk67bTzZYgAAAAAmyCkmpJNPmmRasWjU+ExMx3hmc4yZx1nDjH5r1OBzfT+j5qeG9hz77SpNWuDOJemm3BrEYWMlw5mPwtFtKy2mUGW8ssTsqnFNFJqaWNGMKTVWap9WKKTCk1SI3lNK9JXajRoze1KMovlKLi/RrRk1nU7Tp4lksHGbg+cG4S/ii9H9D3F53SJc3H27LrM1+qfoYafUzW8PSq56RiukUvkePt3lvRAdhCdG5WE6Tp5Xtq+xzGcmnpbCu1fDcfzh8z1vpc/E4sR9pmP9/7czk/Jl/V2nNoWbtUNZSslGCWj5yaX3M98U1ibT4iJlX4kT2h6U5njXWNzmSlFukXiErzY3Ab92+1wh3vf4Hb9LwdV9z7d2lzMmq6b09K5QAAAAAAADjQGezrJ+c61w/aj0/I4nO4H89PDdw5/azOtOLOBemm7E7dnWpIxeExKqxeFcXwLRO2WLGK7GiJhZNovMcwjSfVcY5hXR5WFUaDsBp45tNCeFzDEbq7s7HdFPk1Z3np73Je49pwLxn4tN+YjX9uzk5t48s6KweNuxdlVMYbqnOKm9W2oa95/DUyZq0wY7ZJnxH7+xW85LRWIesuZ4l2dEOYNEOZIotpMjhilBvRWV67rfJxfOL+B0eBzrcaZ94lr58HxY/KHkOzUaJ9pLdcl7CXHR9dTY5vqds1eivaPdTDxYpPVPloXI5LcIlIkMTZesd0t9sbRu0OXjKX0X5nqvS6axzLj8y276X51GoAAAAAAAAAADL7QZcovfiu7Lw6Poef9S4kUnrr4lv8AHy77SoovQ4cw3DlkFJGPwRKmxdG6y8TtlrJFUiswsmVWGOYQkxsKSad3waVub5TVidN9d6PCM1prp080bXG5eTjz8kseXDXJ9RvKslpw7bgtZPhvvTVLouhfk87LyI1ae32Ri49MfePKxcjTZiXIkIciQhyAS5EhLkSEtkpI8UXr5Jej7ML/AJaHqz1/p38CHE5P8SVsbzXAAAAAAAAAABFzOrepmui3l7uJr8unXhtDJitq8MNdHRs8deNS60eDlRhsI+YVarUisr1lT6aMtLKerkUkSISKSF7xA5vA045BJLkSEuRIS5EhDkToJcidBLkBzUkEXxRavkl6PsvLXDR8pP7HrfTJ3h/q4nK/iLc6DXAAAAAAAAAAAm1axkuqa+RW0brMJjyweJj3meKzdrOvXw7WjWssTjF3SseVqqGxcTIzQ7ErIdjIqkreIBvDQ45DQ45E6CXInQQ5E6CXIaCXInQS5E6HNSQqL4iB6HsfPWhrpL6r8j1HpNt45hx+ZHzr46rUAAAAAAAAAABxgYXErvHiOR9Tr08O1o1JXN4z2SKpqoreZkZoN6hJSkRpJW+RoG8BxyGglzJ0EOwnQQ7CdDnaE6Q5vjQ5vE6BvDQVFhLebD2awmvRnofSLfVDl82O8S1J22gAAAAAAAAAADjAw2I9o8PyPqdengqCNSV0fHvgKrVUVz4mVmgy2AKQHd4JG+QEysJ0GLMQl4loqjaNPFoyRjlGzbxiLfClHU7HFofDk6jkb0V6U7OKwjSS1IaCoyI0NrsHb3pLrD7nZ9JnWTX4c/mx2bU9C5oAAAAAAAAAAOS5P0IkYe/2jw/I+p2KeCoGpKyBmcy1F6qO2RkhlMuRYc3gDfGg3ZckTFZk2gYjHdDPTEpNkGeJkzPFIhXckqux+DLdkOSpmvBk9gjWSGoC4YhorNBMpxJhtjXiyZCwxaW2dhIjSWx2Dn+u06xl9Dqel/xY/r/hpcz6G/PSOUAAAAAAAAAABNnsv0f0It4lMeWIt9o8NyPqdengtGrKylzSziZKwy0hT2TMkLmXMnQQ7CelG0e7E6GSuPaJlAsvlJ6LibFaRCkyscu2ftt0bTS8y+/spNohrss2J4J7jfnLSK+Znpw81/EMFuRWPdavZSSXCEfc4l7emZlI5VUDFZG4+1W16rQ1MnGy08wy1y1nxKpxWRwf7Ohi6rV8skWUmN2fktXHiWrlhbamtw863xTMu4lJyjE9THbGtEp9dxhmq226/D2Ddjl4KL+mn3Op6ZT/AJYlpcy3y6egHoHMAAAAAAAAAAAi32Zfwv6FbfTKY8sVZ7R4bkfU69fAm9Ea3utDNZhbxZmiGeqqssMsQbMTtLxVG0a3EGWtFZkrBZfbfLSKenUyx2UmdeW92d2M0SlJf+0uXuXibeDh5MvfxDWy8iK9m2wWWVVJbsU2v2n9uh2MPFx4vEd/u0b5bW8ppssYA40BExGWUz5wSfWPd/I1snExX81/syVy2r7qnFbN/uST8nwZz8vpW/olsV5X3UOY7PS0e/Xw66ar4nPvw8uP2bFc9Z92Xx+yr4uvh5MpE2jzDLF4RcFs9iN9RcXxfqZIx9Uk5IiHrOzGUfo1Wj9uSW95Lodzicf4Vdz5lzc2Xrlcm4wAAAAAAAAAAA5JaprqmRMbgYm32jw/JjVnXp4R8dZpBmrWO7JVlMZbxZsVhmVtthnrVWZR+9J6JN6mWIVmWiyHZKy2Sc0/4f69DPjxXyTqsMN8sVh6TlGz9VMVqk2vD9lf1Ozx+BSne/ef2aGTPNvC5N9rgAAAAAAAABqeGrfOEX57q1MdsVLeawtFpjxIqw8I+zGMfNJJk1x0r9MRCJtM+ZOl0AAAAAAAAAAAAADH5rTuWyXm9PR8jyPqOGaZZdTBbdYU+ZPVaHOpDPDN4jDvU2ohbZOEySy2XLRdWZq1mVbXiG7yDY+MEpTWnqu8/ReB1OP6fa3e/aP3aWXk+0NdRRGC3YpJfX1Oxjx1xxqsaaVrTadydLoAAAAAAAAAAAAAAAAAAAAAAAAAAAAQM0y5WrVcJLk/BrozT5fEjPH5ZcWWaSzmIyieujXzRwbem5KzrTejkVmD2E2Ybeskorz0k/gjbw+l3n6p0xX5UezQYLLa6tN1av8AefP3dDr4eLjxeI7/AHat8treUw2GMAAAAAAAAAAAAAAAAAAAAAAH/9k="

def response(flow: http.HTTPFlow):
    global time_spent, points, lesson, auto_answer
    url = flow.request.pretty_url

    if "api.bedrocklearning.org/api/students" in url and "dashboard" in url:
        try:
            data = json.loads(flow.response.content.decode("utf-8"))
            data["firstname"] = f"{data.get('firstname', '')} (Star)"
            data["points"] = points
            data["pointsWeek"] = points
            data["time"] = time_spent
            data["timeweek"] = time_spent
            data["lesson"] = lesson
            flow.response.content = json.dumps(data).encode("utf-8")
        except:
            pass

    if "api.bedrocklearning.org/api/notifications/" in url:
        flow.response.content = json.dumps({
            "count": 999,
            "unread": 999,
            "items": []
        }).encode("utf-8")

    if "https://api.bedrocklearning.org/api/learningcontent" and "/submit" in url and flow.request.method == "POST":
        if auto_answer == True:
            response_text = flow.response.content.decode('utf-8')
            data = json.loads(response_text)

            new_data = {
        "success": True,
        "tryagain": False,
        "audio": data['audio'],
        "message": data['message'],
        "image": data['image'],
        "studentResponse": data['studentResponse'],
        "correctResponse": data['correctResponse'],
        "hideFeedback": data['hideFeedback'],
        "lessonFinished": data['lessonFinished'],
        "endWithResults": data['endWithResults'],
        "stage": data['stage'],
        "topicFeedback": data,
        "oneOffActivity": data['oneOffActivity'],
    }
            flow.response.content = json.dumps(new_data).encode('utf-8')

class MitmAddon:
    def request(self, flow): request(flow)
    def response(self, flow): response(flow)

async def run_proxy():
    opts = options.Options(listen_host='127.0.0.1', listen_port=8082, ssl_insecure=True)
    master = DumpMaster(opts, with_termlog=False, with_dumper=False)
    master.addons.add(MitmAddon())
    await master.run()

def start_proxy():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try: loop.run_until_complete(run_proxy())
    except KeyboardInterrupt: pass
    finally: loop.close()

def menu():
    global time_spent, points, lesson, auto_answer
    while True:
        clear()
        print_header()
        print(f" Current Values:")
        print(f"   → Time Spent : {time_spent}")
        print(f"   → Points     : {points}")
        print(f"   → Lesson     : {lesson}")
        print(f"   → Auto Answer : {'Enabled' if auto_answer == True else 'Disabled'}")
        print()
        print_menu()
        try:
            choice = int(input(" Enter your choice: "))
            print()
            if choice == 0:
                time_spent = int(input("  Set Time Spent: "))
            elif choice == 1:
                points = int(input("  Set Points: "))
            elif choice == 2:
                lesson = int(input("  Set Lesson: "))
            elif choice == 3:
                if auto_answer == False:
                    auto_answer = True
                else:
                    auto_answer = False
            elif choice == 4:
                clear()
                break
            elif choice == 5:
                print("\nExiting...\n")
                time.sleep(1)
                exit()
        except:
            print(" Invalid input. Try again.")
            time.sleep(1.5)

if __name__ == "__main__":
    clear()
    menu()
    set_proxy()
    print_header()
    print(" Proxy is now active on 127.0.0.1:8082.")
    print(" Press Ctrl+C to stop.\n")
    proxy_thread = threading.Thread(target=start_proxy, daemon=True)
    proxy_thread.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down proxy...")