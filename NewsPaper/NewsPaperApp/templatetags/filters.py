from django import template

register = template.Library()


@register.filter(name='censor')
def censor(value):
    censored, default = '', value.split()
    file = open('NewsPaperApp/templatetags/censor_list.txt', 'r', encoding='utf8')
    text = file.read().split(', ')
    file.close()
    for word in default:
        for cen in text:
            if cen in word:
                word = word[0] + '*' * (len(word) - 1)
        censored += word + ' '
    return censored
