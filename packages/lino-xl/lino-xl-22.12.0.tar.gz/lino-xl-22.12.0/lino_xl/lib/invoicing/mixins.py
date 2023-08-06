# -*- coding: UTF-8 -*-
# Copyright 2016-2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.db import models
from datetime import timedelta
from etgen.html import E, join_elems
from lino.api import dd, _, gettext
from lino.core.gfks import gfk2lookup
from lino_xl.lib.ledger.utils import ZERO
from lino_xl.lib.cal.utils import day_and_month
from lino_xl.lib.cal.choicelists import DurationUnits
from lino.utils import ONE_DAY

from django.contrib.contenttypes.fields import GenericRelation

MAX_SHOWN = 3  # maximum number of invoiced events shown in invoicing_info

class Periodicity(dd.Choice):
    renew_every = None
    renew_unit = None
    renew_before = None

    def __init__(self, value, text, renew_unit, renew_every, renew_before):
        super(Periodicity, self).__init__(value, text, value)
        self.renew_unit = renew_unit
        self.renew_every = renew_every
        self.renew_before = renew_before

class Periodicities(dd.ChoiceList):
    item_class = Periodicity

add = Periodicities.add_item
add("m", _("Monthly"), DurationUnits.months, 1, 7)
add("q", _("Quarterly"), DurationUnits.months, 3, 14)
add("y", _("Yearly"), DurationUnits.years, 1, 28)


class InvoicingInfo(object):
    invoiced_qty = ZERO
    invoiced_events = 0
    used_events = []
    invoicings = None
    invoicing_min_date = None
    invoicing_max_date = None
    # tariff = None
    # 20210724
    invoiceable_product = None
    invoiceable_qty = None
    asset_to_buy = None
    number_of_events = None
    min_asset = None
    max_asset = None

    def __init__(self, enr, min_date, max_date):
        # print("20220507 InvoicingInfo()", enr)
        self.generator = enr
        self.min_date = min_date
        self.max_date = max_date

        max_date = self.max_date or dd.today()
        end_date = enr.get_invoiceable_end_date()
        if end_date:
            max_date = min(max_date, end_date)

        start_date = enr.get_invoiceable_start_date(max_date)

        state_field = dd.plugins.invoicing.voucher_model._meta.get_field(
            'state')
        vstates = state_field.choicelist.get_editable_states()
        qs = enr.invoicings.exclude(voucher__state__in=vstates)
        product = enr.get_invoiceable_product(max_date)
        if product is not None:
            qs = qs.filter(product=product)
        self.invoicings = qs
        self.invoiceable_qty = enr.get_invoiceable_qty()

        sub = enr.get_invoicing_periodicity(product)
        if sub is not None:
            last_invoicing = self.invoicings.last()
            if last_invoicing is None:
                # next_date = enr.get_invoiceable_start_date(max_date)
                paid_until = start_date - ONE_DAY
            else:
                paid_until = last_invoicing.voucher.invoicing_max_date
            next_date = paid_until - timedelta(days=sub.renew_before)
            if next_date < max_date:
                # next invoicing date not yet reached
                return
            self.asset_to_buy = 1
            self.invoicing_min_date = paid_until + ONE_DAY
            self.invoicing_max_date = sub.renew_unit.add_duration(
                paid_until, sub.renew_every)
            # self.invoiceable_product = product
            return

        self.invoiced_events = enr.get_invoiceable_free_events() or 0
        self.used_events = list(enr.get_invoiceable_events(
            start_date, max_date))

        tariff = enr.get_invoicing_pass_type(product)
        if tariff is not None:
            self.number_of_events = tariff.number_of_events
            self.min_asset = tariff.min_asset
            self.max_asset = tariff.max_asset
            # every invoiceable creates one invoicing
            # self.invoiceable_product = product
            # self.invoiceable_qty = enr.get_invoiceable_qty()
            # dd.logger.info("20181116 e no tariff")
            # return

        for obj in self.invoicings:
            # tariff = getattr(obj.product, 'tariff', None)
            # if tariff:
            if obj.qty is not None:
                self.invoiced_qty += obj.qty
                if self.number_of_events:
                    self.invoiced_events += int(obj.qty * self.number_of_events)
        # print("20220507 invoiced, invoiceable qty", self.invoiced_qty, self.invoiceable_qty)

        # print("20181116 f %s", self.tariff.number_of_events)
        if self.number_of_events:
            asset = self.invoiced_events - len(self.used_events)
            # dd.logger.info(
            #     "20220507 %s %s %s %s",
            #     start_date, max_date, asset, self.min_asset)
            if end_date and end_date < max_date and asset >= 0:
                # ticket #1040 : a participant who declared to stop before
                # their asset got negative should not get any invoice for
                # a next asset
                return

            if self.min_asset is None:
                self.asset_to_buy = - asset
            elif asset > self.min_asset:
                return  # nothing to invoice
            else:
                self.asset_to_buy = self.min_asset - asset

            if self.max_asset is not None:
                self.asset_to_buy = min(self.asset_to_buy, self.max_asset)

        # removed 20220507 because i don't see why it was:
        # elif self.invoiced_qty <= 0:
        #     self.asset_to_buy = 1
        elif self.invoiceable_qty in (None, ''):
            return
        else:
            self.invoiceable_qty -= self.invoiced_qty
            if self.invoiceable_qty <= 0:
                return
            # self.asset_to_buy = self.invoiceable_qty - self.invoiced_qty
            # # print("20220507 self.asset_to_buy", self.asset_to_buy)
            # if self.asset_to_buy <= 0:
            #     return

        # qty = self.asset_to_buy * enr.get_invoiceable_qty()

        # 20210724
        self.invoiceable_product = product
        # self.invoiceable_qty = qty
        # self.asset_to_buy = asset_to_buy


    def __str__(self):
        return "{}({})".format(self.__class__.__name__, self.__dict__)

    def format_as_html(self, ar):
        elems = []
        if len(self.used_events) == 0:
            return E.p(gettext("No invoiced events"))
        # used_events = list(self.used_events)
        invoiced = self.used_events[self.invoiced_events:]
        coming = self.used_events[:self.invoiced_events]

        fmt = self.generator.get_invoiceable_event_formatter()
        # def fmt(ev):
        #     return self.generator.format_invoiceable_event(ev, ar)

        if len(invoiced) > 0:
            elems.append("{0} : ".format(_("Invoiced")))
            if len(invoiced) > MAX_SHOWN:
                elems.append("(...) ")
                invoiced = invoiced[-MAX_SHOWN:]
            elems += join_elems(map(fmt, invoiced), sep=', ')
            # s += ', '.join(map(fmt, invoiced))
            # elems.append(E.p(s))
        if len(coming) > 0:
            if len(elems) > 0:
                elems.append(E.br())
            elems.append("{0} : ".format(_("Not invoiced")))
            elems += join_elems(map(fmt, coming), sep=', ')
            # s += ', '.join(map(fmt, coming))
            # elems.append(E.p(s))
        return E.p(*elems)

    def invoice_number(self, voucher):
        # used by lino_voga.courses.Course
        if self.invoicings is None:
            return 0
        n = 1
        for item in self.invoicings:
            n += 1
            if voucher and item.voucher.id == voucher.id:
                break
        # note that voucher.id is None when we are generating the
        # invoice, and then we return the next available number
        return n



# class InvoicingOrder(dd.Model):
#
#     class Meta:
#         abstract = True
#
#     def get_invoicing_area(self):
#         return rt.models.invoicing.Area.objects.first()
#         # e.g. in Presto: return self.journal.room.invoicing_area
#         # return None


class InvoiceGenerator(dd.Model):
    # event_date_field = None

    _invoicing_info = None
    default_invoiceable_qty = 1

    class Meta:
        abstract = True

    if dd.is_installed("invoicing"):
        invoicings = GenericRelation(
            dd.plugins.invoicing.item_model,
            content_type_field='invoiceable_type',
            object_id_field='invoiceable_id')

    # @classmethod
    # def on_analyze(cls, site):
    #     super(InvoiceGenerator, cls).on_analyze(site)
    #     de = cls.get_data_elem(cls.event_date_field)
    #     def func(self):
    #         return de.value_from_object(self)
    #     cls.get_invoiceable_event_date = func
    #     # if isinstance(cls.invoiceable_date_field, six.string_types):
    #     #     cls.invoiceable_date_field =

    def get_invoicing_area(self):
        return rt.models.invoicing.Area.objects.first()
        # raise NotImplementedError()
        # return None
        # no longer overridden in Presto: return self.journal.room.invoicing_area
        # overridden in orders.Order

    def get_invoicings(self, **kwargs):
        # deprecated. use invoicings instead.
        item_model = dd.plugins.invoicing.item_model
        # item_model = rt.models.sales.InvoiceItem
        kwargs.update(gfk2lookup(item_model.invoiceable, self))
        return item_model.objects.filter(**kwargs)

    def get_last_invoicing(self):
        return self.invoicings.order_by('voucher__voucher_date').last()

    def allow_group_invoices(self):
        return True

    def get_invoice_items(self, info, invoice, ar):

        # print("20220507 get_invoice_items()", self,
        #     info.invoiceable_product, info.invoiceable_qty,
        #     info.number_of_events)
        # 20210724
        if info.invoiceable_product is None:
            return

        # invoiceable_qty = self.get_invoiceable_qty()
        if info.invoiceable_qty is None:
            return

        # 20210724
        kwargs = dict(product=info.invoiceable_product)
        # 20210804 kwargs = dict(invoiceable=self, product=info.invoiceable_product)
        # kwargs = dict(invoiceable=self)

        if info.number_of_events is None:
            # qty = asset_to_buy * info.invoiceable_qty
            qty = info.invoiceable_qty
            kwargs.update(
                title=self.get_invoiceable_title(), qty=qty)
            i = invoice.add_voucher_item(**kwargs)
            i.discount_changed(ar)
            yield i
            return

        asset_to_buy = info.asset_to_buy
        if asset_to_buy is None:
            return

        # sell the asset in chunks

        number = info.invoiced_events // info.number_of_events
        while asset_to_buy > 0:
            number += 1
            kwargs.update(
                title=self.get_invoiceable_title(number), qty=info.invoiceable_qty)
            i = invoice.add_voucher_item(**kwargs)
            i.discount_changed(ar)
            yield i
            asset_to_buy -= info.number_of_events

    def get_invoiceable_title(self, number=None):
        return str(self)

    def compute_invoicing_info(self, min_date, max_date):
        if self._invoicing_info is None \
           or self._invoicing_info.min_date != min_date \
           or self._invoicing_info.max_date != max_date:
            self._invoicing_info = InvoicingInfo(self, min_date, max_date)
        # assert self._invoicing_info.generator is self
        return self._invoicing_info

    @dd.displayfield(_("Invoicing info"))
    def invoicing_info(self, ar):
        info = self.compute_invoicing_info(None, dd.today())
        return info.format_as_html(ar)

    def get_invoiceable_product(self, max_date=None):
        return None

    def get_invoiceable_qty(self):
        return self.default_invoiceable_qty

    def get_invoicing_pass_type(self, product=None):
        if product is not None:
            return product.tariff
        return None

    def get_invoicing_periodicity(self, product):
        return

    def get_invoiceable_end_date(self):
        # todo: return None here (but have existing children return self.end_date)
        return self.end_date

    def get_invoiceable_start_date(self, max_date):
        # don't look at events before this date.
        return None

    def get_invoiceable_events(self, start_date, max_date):
        yield self

    def get_invoiceable_event_formatter(self):
        def fmt(ev, ar=None):
            txt = day_and_month(ev.start_date)
            if ar is None:
                return txt
            return ar.obj2html(ev, txt)
        return fmt

    def get_invoiceable_free_events(self):
        return 0

    # def get_invoiceable_amount(self, ie):
    #     return ie.amount

    # def get_invoiceable_event_date(self, ie):
    #     return ie.start_date

    # def get_invoiceable_amount(self):
    #     return None

    def get_invoiceable_partner(self):
        return None

    def get_invoiceable_payment_term(self):
        return None

    def get_invoiceable_paper_type(self):
        return None

    @classmethod
    def get_generators_for_plan(cls, plan, partner=None):
        return cls.objects.all()

    def setup_invoice_from_suggestion(self, invoice, plan, info):
        if info.invoicing_max_date is not None:
            invoice.invoicing_min_date = info.invoicing_min_date
            invoice.invoicing_max_date = info.invoicing_max_date
        else:
            invoice.invoicing_min_date = plan.min_date
            invoice.invoicing_max_date = plan.get_max_date()

    def setup_invoice_item(self, item):
        pass

    @classmethod
    def filter_by_invoice_recipient(cls, qs, partner, fieldname):
        q1 = models.Q(**{
            fieldname + '__salesrule__invoice_recipient__isnull': True,
            fieldname:partner})
        q2 = models.Q(**{
            fieldname+'__salesrule__invoice_recipient':partner})
        return qs.filter(models.Q(q1 | q2))
