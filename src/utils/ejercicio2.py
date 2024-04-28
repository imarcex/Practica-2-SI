from utils.internal_interfaces import __get_all_critical_users

def get_critical_users_clicked_spam(sampleLength: int, above_fifty_percent: bool):
    critical_users = __get_all_critical_users()
    print(critical_users)
    critical_users['perone'] = critical_users['cliclados'] / critical_users['total']

    if above_fifty_percent:
        criba = critical_users[critical_users['perone'] > 0.5]
    else:
        criba = critical_users[critical_users['perone'] < 0.5]
    
    criba['percent'] = str(criba['perone']* 100) + '%'
    
    usuario_percent = criba[["username", "percent"]][:sampleLength]
    
    return list(usuario_percent.itertuples(index=False, name=None))
