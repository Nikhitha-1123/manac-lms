# Task: Allow interns to download offer letter and remove accept offer button

## Steps to Complete

- [ ] Install reportlab library for PDF generation
- [ ] Edit lms/templates/lms/offer_letter.html: Remove the "Accept Offer" button and its conditional logic, update "Download PDF" button to link to new download URL
- [ ] Edit lms/views.py: Add new `download_offer_letter` view to generate and return PDF
- [ ] Edit lms/urls.py: Add URL pattern for the download view
- [x] Test the PDF download functionality
