from utils.internal_interfaces import __get_all_critical_users, __get_n_outdated_webs

def get_n_crtitical_users(sampleLength):
    critical_users = __get_all_critical_users()[:sampleLength]

    return critical_users['username'].to_list()

def get_n_outdated_webs(sampleLength):
    top_webs_politicas_desactualizadas = __get_n_outdated_webs(sampleLength)

    return top_webs_politicas_desactualizadas['web'].to_list()