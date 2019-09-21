function Account() {
    var self = this;
    self.accountWrapper = $('.add-account-wrapper');
    self.curryWrapper = $('.account-curry-wrapper');
    self.totalProperty = $('.property-total-wrapper');
    self.detailsProperty = $('.property-details-wrapper');

};


Account.prototype.run = function () {
    var self = this;
    self.listenShowHideAddAccount();
    self.listenShowHideCurryWrapper();
    self.listPropertyTotalShowHideEvent();
    self.listenPropertyDetailsShowEvent();
    self.listtenToalAccountCloseEvent();
    self.listtenPropertyDetailsCloseEvent();
    self.deleteAccount();
    self.listenSubmitAccount();
    self.listendenominationEvent();
    // self.listenEditAccount();

}

Account.prototype.listenShowHideAddAccount = function () {
    var self = this;
    var closeBtn = $('.close-btn');
    $('#add-account-btn').click(function () {
        self.accountWrapper.show()
    });
    $('.update-property').on('click', function () {
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        self.accountWrapper.show()
        xfzajax.post({
            'url': '/deal/accountinfo/',
            'data': {
                'pk': pk,
            }
        })
    })
    closeBtn.click(function () {
        self.accountWrapper.hide()
    });

};


Account.prototype.listendenominationEvent = function () {

    $('#account-curry-configuration').on('click', function () {
        $('.denomination-mask-account-wrapper').show();
        $('.denomination-account-wrapper').show();
    })

    $('.denomination-close-btn').on('click', function () {
        $('.denomination-mask-account-wrapper').hide();
        $('.denomination-account-wrapper').hide();

    })
}

Account.prototype.listPropertyTotalShowHideEvent = function () {
    var self = this;
    var closeBtn = $('.close-btn');
    $('#property-total').click(function () {
        self.totalProperty.show()
    });
    closeBtn.click(function () {
        self.totalProperty.hide()
    })

};

Account.prototype.listenShowHideCurryWrapper = function () {
    var self = this;
    var closeBtn = $('.close-btn');
    $('.add-property').click(function () {
        self.curryWrapper.show()
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        self.chargeAccountEvent(pk)
    });
    closeBtn.click(function () {
        self.curryWrapper.hide();
    })
    
};

Account.prototype.listtenToalAccountCloseEvent = function () {
    $('.property-close-btn').on('click', function () {
        $('.property-total-wrapper').hide()
    })
};

Account.prototype.listtenPropertyDetailsCloseEvent = function () {
    $('.property-close-btn').on('click', function () {
        $('.property-details-wrapper').hide()
    })
};

Account.prototype.listenPropertyDetailsShowEvent = function () {
    var self = this;
    var closeBtn = $('.close-btn');
    $('.check-property').on('click', function () {
        self.detailsProperty.show()
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        // console.log(pk)
        xfzajax.post({
            'url': '/deal/showassert/',
            'data': {
                'pk': pk
            },
            // 'success': function (result) {
            //     console.log("suceesee")
            //     console.log(result)
            //     if (result['code'] === 200) {
            //         datas = result['data']
            //         console.log(datas['Platform_name'])
            //         console.log(datas['asset_change'])
            //         console.log(datas['assets_dict'])
            //         console.log(datas['history_profit'])
            //     }
            // }
        });
    });
    closeBtn.click(function () {
        self.detailsProperty.hide();
    })

}

Account.prototype.deleteAccount = function () {
    var self = this;
    $('.delete-property').on('click', function () {
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        xfzalert.alertConfirm({
            'title': '您确定删除这个账户吗？',
            'confirmCallback': function () {
                xfzajax.post({
                    'url': '/deal/deleteaccount/',
                    'data': {
                        'pk': pk,
                    },
                    'success': function (result) {
                        if (result['code'] === 200) {
                            console.log(result)
                            window.location.reload()
                        }
                    }
                })
            }
        })
    })
}

Account.prototype.listenEditAccount = function () {
    var self = this;
    $('.update-property').on('click', function () {
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        var account = $('.account-body');
        platform = $('#platform').find("option:selected").val()
        title = account.find("input[name='account-name']").val()
        accesskey = account.find("input[name='access']").val()
        secretkey = account.find("input[name='scrent']").val()
        var url = ''
        if (pk) {
            url = '/deal/editaccount/'
        } else {
            url = '/deal/addaccount/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'platform': platform,
                'title': title,
                'accesskey': accesskey,
                'secretkey': secretkey,
                'pk': pk,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess("添加账户成功！", function () {
                        window.location.reload()
                    });
                }
            }
        });

    })

}
Account.prototype.listenSubmitAccount = function () {
    var confirmBtn = $('.confirm');

    confirmBtn.click(function () {
        var currentbtn = $(this);
        var tr = currentbtn.parent().parent();
        var pk = tr.attr('data-id');
        var account = $('.account-body');
        platform = $('#platform').find("option:selected").val()
        title = account.find("input[name='account-name']").val()
        accesskey = account.find("input[name='access']").val()
        secretkey = account.find("input[name='scrent']").val()
        var url = ''
        if (pk) {
            url = '/deal/editaccount/'
        } else {
            url = '/deal/addaccount/'
        }
        xfzajax.post({
            'url': url,
            'data': {
                'platform': platform,
                'title': title,
                'accesskey': accesskey,
                'secretkey': secretkey,
                'pk': pk,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess("添加账户成功！", function () {
                        window.location.reload()
                    });
                }
            }
        });
    });
}

Account.prototype.chargeAccountEvent = function (pk) {
    var confirmBtn = $('.curry-confirm')
    confirmBtn.click(function () {
        num = $('#currency-number').val()
        currency = $('#currency').val()
        console.log("*")
        console.log(num, currency, pk)
        xfzajax.post({
            'url': '/deal/chargeaccount/',
            'data': {
                'pk': pk,
                'num': num,
                'currency': currency,
            },
            'success': function (result) {
                if (result['code'] === 200) {
                    xfzalert.alertSuccess("增资成功", function () {
                        window.location.reload();
                    })
                }
            }
        })
    })
}


$(function () {
    var account = new Account();
    account.run();
})