# -*- coding: utf-8 -*-
from django.template import RequestContext
import os
from django.http import HttpResponse
from django.template.loader import select_template
from django_xhtml2pdf.utils import generate_pdf_template_object

class Xhtml2PdfResponseMixin(object):
    """
    Example usage:

    >>> from django.views.generic import DetailView
    >>> from django_xhtml2pdf.views.generic import Xhtml2PdfResponseMixin
    >>>
    >>> class PdfView(Xhtml2PdfResponseMixin, DetailView):
    >>>     template_name = 'reports/simple-test.html'
    >>>     model = AnyModel

    Notice:

    Xhtml2PdfResponseMixin must be the first parent to overwrite the render_to_response method.
    """
    response_class = HttpResponse
    filename = None
    attachment = False

    def get_filename(self, template = None):
        if not self.filename:
            filename = '{0}.pdf'.format(os.path.splitext(os.path.basename(template.name))[0])
        else:
            filename = self.filename
        return filename

    def render_to_response(self, context, **response_kwargs):
        context = RequestContext(self.request, context)
        resp = self.response_class(content_type='application/pdf')
        template = select_template(self.get_template_names())
        generate_pdf_template_object(template, resp, context)
        self.filename = self.get_filename(template)
        if self.attachment:
            att = 'attachment; '
        else:
            att = ""
        resp['Content-Disposition'] = '{0}filename={1}'.format(att, self.filename)
        return resp
