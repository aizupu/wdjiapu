import datetime
from django.shortcuts import render, redirect
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from home.models import UserIP, VisitNumber, DayNumber

def split_page(request,mylist):
    paginator = Paginator(mylist, 10)
    page_num = request.GET.get('page', default='1')
    try:
        page = paginator.page(page_num)
    except PageNotAnInteger as e:
        # 不是整数返回第一页数据
        page = paginator.page('1')
        page_num = 1
    except EmptyPage as e:
        # 当参数页码大于或小于页码范围时,会触发该异常
        print('EmptyPage:{}'.format(e))
        if int(page_num) > paginator.num_pages:
            # 大于 获取最后一页数据返回
            page = paginator.page(paginator.num_pages)
        else:
            # 小于 获取第一页
            page = paginator.page(1)

    # 这部分是为了再有大量数据时，仍然保证所显示的页码数量不超过10，
    page_num = int(page_num)
    if page_num < 6:
        if paginator.num_pages <= 10:
            dis_range = range(1, paginator.num_pages + 1)
        else:
            dis_range = range(1, 11)
    elif (page_num >= 6) and (page_num <= paginator.num_pages - 5):
        dis_range = range(page_num - 5, page_num + 5)
    else:
        dis_range = range(paginator.num_pages - 9, paginator.num_pages + 1)
    return page,paginator,dis_range

 
# 自定义的函数，不是视图
def change_info(request, end_point):
    """
    # 修改网站访问量和访问 ip 等信息
    # 每一次访问，网站总访问次数加一
    """
    count_nums = VisitNumber.objects.filter(id=1)
    if count_nums:
        count_nums = count_nums[0]
        count_nums.count += 1
    else:
        count_nums = VisitNumber()
        count_nums.count = 1
    count_nums.save()
 
    # 记录访问 ip 和每个 ip 的次数
    if 'HTTP_X_FORWARDED_FOR' in request.META:  # 获取 ip
        client_ip = request.META['HTTP_X_FORWARDED_FOR']
        client_ip = client_ip.split(",")[0]  # 所以这里是真实的 ip
    else:
        client_ip = request.META['REMOTE_ADDR']  # 这里获得代理 ip
    # print(client_ip)
 
    ip_exist = UserIP.objects.filter(ip=str(client_ip), end_point=end_point)
    if ip_exist:  # 判断是否存在该 ip
        uobj = ip_exist[0]
        uobj.count += 1
    else:
        uobj = UserIP()
        uobj.ip = client_ip
        uobj.end_point = end_point
        uobj.count = 1
    uobj.save()
    
    # 增加今日访问次数
    date = datetime.date.today()
    today = DayNumber.objects.filter(day=date)
    if today:
        temp = today[0]
        temp.count += 1
    else:
        temp = DayNumber()
        temp.dayTime = date
        temp.count = 1
    temp.save()