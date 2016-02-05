from django.core.management.base import NoArgsCommand

from kuma.wiki.models import Document


class Command(NoArgsCommand):
    help = "Populate m2m relations for documents and their attachments"

    def handle(self, *args, **options):
        documents = (Document.admin_objects.filter(attachments_populated=False)
                                           .only('pk', 'html'))
        self.stdout.write("Populating document attachments "
                          "for %s documents...\n\n" % documents.approx_count())
        for document in documents.iter_smart(report_progress=True):
            document.populate_attachments(update_populated_field=True)
