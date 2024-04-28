from internal_interfaces import __get_all_critical_users, __get_n_outdated_webs

def get_n_crtitical_users(sampleLength):
    critical_users = __get_all_critical_users()[:sampleLength]

    return {
        "title" : f"Los {sampleLength} usuarios más críticos",
        "xdata" : critical_users['username'].to_list(),
    }

def get_n_outdated_webs(sampleLength):
    top_webs_politicas_desactualizadas = __get_n_outdated_webs(sampleLength)

    return {
        "title" : f"Top {sampleLength} Páginas Web con más Políticas Desactualizadas",
        "xdata" : top_webs_politicas_desactualizadas['web'].to_list(),
    }