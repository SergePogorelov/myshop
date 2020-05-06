import weasyprint
from io import BytesIO

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .models import OrderItem, Order
from .forms import OrderCreateForm
from cart.cart import Cart
from .tasks import order_created


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, 
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                )
            cart.clear()
            # Создание электронного сообщения.
            subject = 'My Shop - Invoice no. {}'.format(order.id)
            message = 'Please, find attached the invoice for your recent purchase.'
            email = EmailMessage(subject, message, 'admin@myshop.com', [order.email])
            # Формирование PDF.
            html = render_to_string('orders/order/pdf.html', {'order': order})
            out = BytesIO()
            weasyprint.HTML(string=html).write_pdf(out, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
            # Прикрепляем PDF к электронному сообщению.
            email.attach(f"order_{order.id}.pdf", out.getvalue(), 'application/pdf')
            email.send()

            # Запуск асинхронной задачи.
            order_created.delay(order.id)
            return render(
                request,
                'orders/order/created.html',
                {'order': order}
        )
    else:
        form = OrderCreateForm()
    return render(
        request,
        'orders/order/create.html', 
        {'cart': cart, 'form': form}
    )


@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render (request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename='f"order_{order.id}.pdf"
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT + 'css/pdf.css')])
    return response
    