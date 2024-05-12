import threading, subprocess, argparse

parser = argparse.ArgumentParser(description="Run ffuf commands on multiple URLs with threading.")
parser.add_argument("-l", "--list", help="List of URLs to scan", required=True)
args = parser.parse_args()

ffuf_command = "ffuf -u fuzztarget/FUZZ -w ~/wordlists/onelistforallmicro.txt -timeout 10 -t 500"
uni = "./uni.sh"
notify = "notify -p discord -id vectra -bulk"
num_threads = 7 # // Number of threads

def clean(text):
    return text.replace("https://", "").replace("http://", "").replace("/", "")

def run_command(ffuf_command, uni, notify, base_url):
    if base_url != "":
        ffuf_command = ffuf_command.replace("fuzztarget", base_url)
        output_file = f"{clean(base_url)}.txt"
        command = f"{ffuf_command} | {uni} | tee {output_file}; echo \"{base_url}\\n$(cat {output_file})\" | {notify}"#; rm {output_file}"
        subprocess.run(command, shell=True, check=True)
        print(command)

def thread_function(url_list):
    for url in url_list:
        run_command(ffuf_command, uni, notify, url)

print(args.list)
urls = open(args.list, "r").read().split("\n")
threads = []

url_chunks = [urls[i::num_threads] for i in range(num_threads)]

for i in range(num_threads):
    thread = threading.Thread(target=thread_function, args=(url_chunks[i],))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
