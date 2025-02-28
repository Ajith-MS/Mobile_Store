from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Payment
import paypalrestsdk

# Configure PayPal SDK
paypalrestsdk.configure({
    "mode": settings.PAYPAL_MODE,  # "sandbox" for testing, "live" for production
    "client_id": settings.PAYPAL_CLIENT_ID,
    "client_secret": settings.PAYPAL_SECRET,
})

def create_payment(request):
    if request.method == "POST":
        total_amount = request.POST.get("amount")

        # Create PayPal payment request
        payment = paypalrestsdk.Payment({
            "intent": "sale",
            "payer": {
                "payment_method": "paypal"
            },
            "redirect_urls": {
                "return_url": request.build_absolute_uri(reverse('payment_success')),
                "cancel_url": request.build_absolute_uri(reverse('payment_cancel')),
            },
            "transactions": [{
                "amount": {
                    "total": total_amount,
                    "currency": "USD"
                },
                "description": "Payment for services"
            }]
        })

        # If PayPal payment is created successfully
        if payment.create():
            print("✅ PayPal Payment Created:", payment.to_dict())

            # Store payment details in DB
            new_payment = Payment.objects.create(
                user=request.user,
                total_amount=total_amount,
                payment_method="PayPal",
                payment_complete=False,
                paypal_payment_id=payment.id
            )
            new_payment.save()

            # Redirect to PayPal approval page
            for link in payment.links:
                if link.rel == "approval_url":
                    return redirect(link.href)

        else:
            print("❌ PayPal Payment Creation Failed:", payment.error)
            return render(request, "error.html", {"error": payment.error})

    return render(request, "payment_form.html")


def payment_success(request):
    """Handles payment success response from PayPal"""
    payment_id = request.GET.get("paymentId")
    payer_id = request.GET.get("PayerID")

    print(f"🔹 Received paymentId: {payment_id}, PayerID: {payer_id}")

    if not payment_id or not payer_id:
        return render(request, "error.html", {"error": "Invalid payment response from PayPal."})

    try:
        payment = paypalrestsdk.Payment.find(payment_id)
        print("✅ Payment Found:", payment.to_dict())

        if payment.execute({"payer_id": payer_id}):
            print("✅ Payment Executed Successfully!")

            # Update Payment record in database
            payment_record = Payment.objects.get(paypal_payment_id=payment_id)
            payment_record.payment_complete = True
            payment_record.save()

            return render(request, "success.html", {"payment": payment_record})
        else:
            print("❌ Payment Execution Failed:", payment.error)
            return render(request, "error.html", {"error": payment.error})

    except paypalrestsdk.ResourceNotFound as e:
        print("❌ PayPal Resource Not Found:", str(e))
        return render(request, "error.html", {"error": "Payment not found. Please try again."})

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        return render(request, "error.html", {"error": str(e)})


def payment_cancel(request):
    return render(request, "cancel.html")


def refund_payment(request, payment_id):
    """Process a refund for a PayPal payment."""
    try:
        # Fetch the payment record from your database
        payment_record = Payment.objects.get(paypal_payment_id=payment_id)

        # Find the payment on PayPal
        payment = paypalrestsdk.Payment.find(payment_id)

        if payment and payment.transactions:
            # Get the first sale transaction ID from PayPal's response
            sale_id = payment.transactions[0].related_resources[0].sale.id

            # Perform the refund
            sale = paypalrestsdk.Sale.find(sale_id)
            refund = sale.refund({
                "amount": {
                    "total": str(payment_record.total_amount),  # Refund the full amount
                    "currency": "USD"
                }
            })

            if refund.success():
                print("✅ Refund Successful!", refund.to_dict())
                messages.success(request, "Refund processed successfully.")

                # Optional: Update your database
                payment_record.payment_complete = False  # Mark as refunded
                payment_record.save()

                return render(request, "refund_success.html", {"refund": refund.to_dict()})
            else:
                print("❌ Refund Failed:", refund.error)
                messages.error(request, "Refund failed: " + str(refund.error))
                return render(request, "error.html", {"error": refund.error})

    except paypalrestsdk.ResourceNotFound as e:
        print("❌ PayPal Payment Not Found:", str(e))
        messages.error(request, "Payment not found.")
        return render(request, "error.html", {"error": "Payment not found."})

    except Exception as e:
        print("❌ Unexpected Error:", str(e))
        messages.error(request, str(e))
        return render(request, "error.html", {"error": str(e)})
