# TODO: Fix MultipleObjectsReturned Error in download_offer_letter View

## Steps to Complete:
- [x] Modify the download_offer_letter function in lms/views.py to retrieve the most recent offer letter using filter().order_by('-issued_date').first() instead of get_object_or_404
- [x] Add a check to raise Http404 if no offer letter exists
- [x] Test the fix by running the Django server and accessing the download-offer-letter URL
