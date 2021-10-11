from DockerHandler import DockerHandler

if __name__ == "__main__":
    evidence_name = '0815-2021-data'
    dh = DockerHandler()
    dh.run_log2timeline(evidence_name, verbose=False)
    #dh.run_pinfo(evidence_name, verbose=False)
    #dh.run_psort(evidence_name, verbose=False)
