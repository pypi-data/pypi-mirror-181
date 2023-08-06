from gtja_vintex_qyt import GTJAVintexQyt

if __name__ == "__main__":
    gtja_vintex_qyt = GTJAVintexQyt("13158901580", "990818")
    print(gtja_vintex_qyt.qc0020().data)
    print(gtja_vintex_qyt.qc0021().data)