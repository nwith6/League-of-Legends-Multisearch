import os
import webbrowser
import configparser


banner = """

  ██▓     ▒█████   ██▓        ███▄ ▄███▓ █    ██  ██▓  ▄▄▄█████▓ ██▓  ██████ ▓█████ ▄▄▄       ██▀███   ▄████▄   ██░ ██ 
 ▓██▒    ▒██▒  ██▒▓██▒       ▓██▒▀█▀ ██▒ ██  ▓██▒▓██▒  ▓  ██▒ ▓▒▓██▒▒██    ▒ ▓█   ▀▒████▄    ▓██ ▒ ██▒▒██▀ ▀█  ▓██░ ██▒
 ▒██░    ▒██░  ██▒▒██░       ▓██    ▓██░▓██  ▒██░▒██░  ▒ ▓██░ ▒░▒██▒░ ▓██▄   ▒███  ▒██  ▀█▄  ▓██ ░▄█ ▒▒▓█    ▄ ▒██▀▀██░
 ▒██░    ▒██   ██░▒██░       ▒██    ▒██ ▓▓█  ░██░▒██░  ░ ▓██▓ ░ ░██░  ▒   ██▒▒▓█  ▄░██▄▄▄▄██ ▒██▀▀█▄  ▒▓▓▄ ▄██▒░▓█ ░██ 
 ░██████▒░ ████▓▒░░██████▒   ▒██▒   ░██▒▒▒█████▓ ░██████▒▒██▒ ░ ░██░▒██████▒▒░▒████▒▓█   ▓██▒░██▓ ▒██▒▒ ▓███▀ ░░▓█▒░██▓
 ░ ▒░▓  ░░ ▒░▒░▒░ ░ ▒░▓  ░   ░ ▒░   ░  ░░▒▓▒ ▒ ▒ ░ ▒░▓  ░▒ ░░   ░▓  ▒ ▒▓▒ ▒ ░░░ ▒░ ░▒▒   ▓▒█░░ ▒▓ ░▒▓░░ ░▒ ▒  ░ ▒ ░░▒░▒
 ░ ░ ▒  ░  ░ ▒ ▒░ ░ ░ ▒  ░   ░  ░      ░░░▒░ ░ ░ ░ ░ ▒  ░  ░     ▒ ░░ ░▒  ░ ░ ░ ░  ░ ▒   ▒▒ ░  ░▒ ░ ▒░  ░  ▒    ▒ ░▒░ ░
   ░ ░   ░ ░ ░ ▒    ░ ░      ░      ░    ░░░ ░ ░   ░ ░   ░       ▒ ░░  ░  ░     ░    ░   ▒     ░░   ░ ░         ░  ░░ ░
     ░  ░    ░ ░      ░  ░          ░      ░         ░  ░        ░        ░     ░  ░     ░  ░   ░     ░ ░       ░  ░  ░
"""
padding = 15


def main() -> None:
    config = configparser.ConfigParser(allow_no_value=True); config.read(os.getcwd() + "/config.ini")

    if not verify_config(config):
        return print("Config is invalid, please ensure all keys are correct. Use the 'DEFAULT' and 'Example' sections as a reference.")
    
    while True:
        option = main_menu(config)
        accounts = parse_section(config, option)
        site = site_menu()
        
        for key, value  in accounts.items():
            for account in value:
                uri = create_url(site, key, account)
                if uri == None:
                    continue
                webbrowser.open_new_tab(url=uri)


def main_menu(config: list[str]) -> str:
    sections = config.sections()
    menu = [f"{padding * ' '}{option}" for option in [f"[{i+1}] {section}" for i, section in enumerate(sections)]]

    while True:
        clear(); print(banner)

        for line in menu:
            print(line)
        option = input(" " * padding + ">>> ")

        if option.isdigit() and 0 < int(option) <= len(sections):
            return sections[int(option)-1]
        else:
            clear()


def site_menu() -> str:
    sites = ["op.gg", "leagueofgraphs.com"]
    menu = [f"{padding * ' '}{option}" for option in [f"[{i+1}] {site}" for i, site in enumerate(sites)]]

    while True:
        clear(); print(banner)
        
        for line in menu:
            print(line)
        option = input(" " * padding + ">>> ")

        if option.isdigit() and 0 < int(option) <= len(sites):
            return sites[int(option)-1]
        else:
            clear()


def clear() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def verify_config(config: list[str]) -> bool:
    for section in config.sections():
        for key in config[section]:
            if key not in config['DEFAULT']:
                return False
    return True


def parse_section(config: list[str], option: str) -> dict:
    accounts = {}
    for key in config[option]:
        if len(config[option][key]) > 0:
            accounts[key] = config[option][key].split(",")
    return accounts


def create_url(site: str, region: str, username: str) -> str:
    url = str()
    username = username.replace("#", "-"); username = username.replace(" ", "%20")

    if site == "op.gg":
        return f"https://www.op.gg/summoners/{region}/{username}"
    elif site == "leagueofgraphs.com":
        return f"https://www.leagueofgraphs.com/summoner/{region}/{username}"
    else:
        return None
    

if __name__ == "__main__":
    main()
