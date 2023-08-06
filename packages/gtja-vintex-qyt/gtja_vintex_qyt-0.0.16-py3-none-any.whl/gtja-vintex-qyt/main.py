from gtja_vintex_qyt import GTJAVintexQyt

if __name__ == '__main__':
    vintex_qyt_client = GTJAVintexQyt("vintex_username", "vintex_password")
    vintex_qyt_client.qc0020(page=1, rownum=801)
    return_data = vintex_qyt_client.qc0021(page=1, rownum=801, custid="59766206")
    print(return_data.data)