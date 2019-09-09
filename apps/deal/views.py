from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import View
from .models import Account, Property, LastdayAssets
from django.core.paginator import Paginator
from dealapi.exx.exxService import ExxService
from dealapi.exx.exxMarket import MarketCondition
from .forms import AccountModelForm
from django.db.models import Q

# Create your views here.


class AccountList(View):
    """
    账户列表信息
    """
    def get(self, request):
        page = int(request.GET.get('p', 1))
        user_id = request.session.get("user_id")
        # 获取账户信息
        accounts = Account.objects.filter(users__id=user_id)
        print(accounts)

        # 分页
        paginator = Paginator(accounts, 10)
        page_obj = paginator.page(page)
        context_data = get_pagination_data(paginator, page_obj)
        context = {
            'accounts_list': page_obj.object_list,
            'accounts': accounts,
            'page_obj': page_obj,
            'paginator': paginator,
        }
        context.update(context_data)
        return render(request, 'management/tradingaccount.html', context)


class AddAccount(View):
    """
    添加账户
    """
    def get(self, request):
        model_form = AccountModelForm()
        return render(request, 'management/tradingaccount.html', {'model_form': model_form, 'title': '新增账户'})

    def post(self, request):
        model_form = AccountModelForm(request.POST)
        print('-'*20, model_form)
        if model_form.is_valid():
            model_form.save()
            return redirect('../accountlist/')
        else:
            return render(request, 'management/tradingaccount.html', {'model_form': model_form, 'title': '新增用户'})


class EditAccount(View):
    """
    编辑交易账户
    """
    def get(self, request, id):
        account_obj = Account.objects.filter(id=id).first()
        model_form = AccountModelForm(instance=account_obj)
        return render(request, 'management/tradingaccount.html', {'model_form': model_form, 'title': '编辑账户'})

    def post(self, request, id):
        account_obj = Account.objects.filter(id=id).first()
        model_form = AccountModelForm(request.POST, instance=account_obj)
        if model_form.is_valid():
            model_form.save()
            return redirect('../accountlist/')
        else:
            return render(request, 'management/tradingaccount.html', {'model_form': model_form, 'title': '编辑用户'})


class DeleteAccount(View):
    """
    删除账户
    """
    def get(self, id):
        account_obj = Account.objects.filter(id=id).first()
        account_obj.delete()
        return redirect('../accountlist/')


class ShowAssert(View):
    """
    显示账户资产信息
    """
    def get(self, request, id):
        # 获取账户信息
        account_obj = Account.objects.get(id=id)
        # 账户对应的平台
        platform = account_obj.platform
        # 根据平台调用接口获取数据
        if platform.Platform_name == 'EXX':
            # 创建接口对象
            service_api = ExxService(platform.Platform_name, account_obj.secretkey, account_obj.accesskey)
            # 获取用户的资产信息
            res = service_api.get_balance()
            market_api = MarketCondition()
            # 获取所有行情信息
            res1 = market_api.get_tickers()
        elif platform.Platform_name == 'HUOBI':
            pass

        show_currency = Property.objects.filter(Q(account_id=id) & Q(currency_status='1'))
        lastday_obj = LastdayAssets.objects.filter(account_id=id)
        lastday_assets = 0              # 昨日24时资产
        current_total = 0               # 当前总资产
        original_total = 0              # 初始总资产
        withdraw_record = 0             # 提币
        history_profit = 0              # 历史盈亏
        currency_list = list()          # 币种列表
        transaction_pair = list()       # 交易对
        assets_dict = dict()
        profit_loss_dict = dict()

        for lastday in lastday_obj:
            # 昨日资产
            lastday_assets += float(lastday.lastday_assets)

        for queryset in show_currency:
            # 账户币种所有币种总初始资产
            original_total += float(queryset.original_assets)
            withdraw_record += float(queryset.withdraw_record)
            currency_list.append(queryset.currency)
            transaction_pair.append(queryset.currency.lower() + '_usdt')  # 不同平台参考币种不一样，此处不能写死
            assets_dict[queryset.currency] = dict()
            # 币种的初始资产
            assets_dict[queryset.currency]['original_assets'] = str(queryset.original_assets)

        print(transaction_pair)
        # 获取币种总资产/冻结/可用
        for key, value in res['funds'].items():
            if key in currency_list:
                # 账户所有币种总资产
                current_total += float(value['total'])
                assets_dict[key]['current_assets'] = value['total']
                assets_dict[key]['freeze'] = value['freeze']
                assets_dict[key]['balance'] = value['balance']

        # 获取当前参考价
        for key1, value1 in res1.items():
            if key1 in transaction_pair:
                key = key1.split('_')[0].upper()
                assets_dict[key]['last'] = value1.get('last', 0)
                transaction_pair.remove(key1)

        for item in transaction_pair:
            key = item.split('_')[0].upper()
            assets_dict[key]['last'] = '0'

        # 资产变化
        asset_change = dict()
        asset_change['number'] = current_total - lastday_assets
        asset_change['percent'] = (current_total - lastday_assets)/lastday_assets
        # 历史盈亏
        history_profit = dict()
        history_profit['number'] = current_total+withdraw_record-original_total
        history_profit['percent'] = (current_total+withdraw_record)/original_total
        print(lastday_assets, currency_list, current_total)
        print(assets_dict)
        # asset_dict格式{'币种': {'参考价':""，'可用':""，'冻结':""，'当前总资产':""，'初始资产':""}}
        # profit_loss_dict格式{}
        context = {
            'Platform_name': platform.Platform_name,
            'asset_change': asset_change,
            'original_assets': original_total,
            'history_profit': history_profit,
            'withdraw_record': withdraw_record,
            'assets_dict': assets_dict
        }
        # render(request, 'management/tradingaccount.html', context)


class ShowCollectAsset(View):
    pass


class ChargeAccount(View):
    """
    增资
    """
    def post(self, request, id):
        currency = request.POST.get('currency')
        num = request.POST.get('currency-number')

        if currency:
            # 查找账户对应币种的资产信息
            property_obj = Property.objects.filter(Q(account_id=id) & Q(currency=currency))
            original_assets = property_obj.original_assets + float(num)
            Property.objects.filter(Q(account_id=id) & Q(currency=currency)).update(original_assets=original_assets)


class WithDraw(View):
    """
    提币
    """
    def post(self, request, id):
        currency = request.POST.get('currency')
        num = request.POST.get('currency-number')

        if currency:
            property_obj = Property.objects.filter(Q(account_id=id) & Q(currency=currency))
            original_assets = property_obj.original_assets + float(num)
            Property.objects.filter(Q(account_id=id) & Q(currency=currency)).update(original_assets=original_assets)


class ConfigCurrency(View):
    """
    配置币种
    """
    def post(self, request):
        currency = request.POST.get('currency')
        if currency:
            user_id = request.session.get("user_id")
            # 获取账户信息
            accounts = Account.objects.filter(users__id=user_id)
            # 保存到数据库
            for obj in accounts:
                LastdayAssets.objects.create(currency='currency', account_id=obj.id)
                Property.objects.create(currency='currency', account_id=obj.id)
        currency_info = LastdayAssets.objects.all()
        context = {
            'currency_info': currency_info,
        }
        return render(request, context=context)


def get_pagination_data(paginator, page_obj, around_count=2):
    current_page = page_obj.number
    num_pages = paginator.num_pages

    left_has_more = False
    right_has_more = False

    if current_page <= around_count + 2:
        left_pages = range(1, current_page)
    else:
        left_has_more = True
        left_pages = range(current_page - around_count, current_page)

    if current_page >= num_pages - around_count - 1:
        right_pages = range(current_page + 1, num_pages + 1)
    else:
        right_has_more = True
        right_pages = range(current_page + 1, current_page + around_count + 1)

    return {
        # left_pages：代表的是当前这页的左边的页的页码
        'left_pages': left_pages,
        # right_pages：代表的是当前这页的右边的页的页码
        'right_pages': right_pages,
        'current_page': current_page,
        'left_has_more': left_has_more,
        'right_has_more': right_has_more,
        'num_pages': num_pages
    }
