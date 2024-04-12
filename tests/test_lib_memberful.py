from lxml import html

from jg.coop.lib.memberful import parse_export_id


def test_parse_export_id_members():
    html_tree = html.fromstring(
        """
            <turbo-frame id="modal">
            <div class="sticky top-0 bg-white flex items-start justify-between md:min-w-[460px] gap-8 border-b pb-4 pt-6 mx-8 mb-4">
                <div class="flex flex-col gap-1">
                <h2 class="text-2xl font-semibold">Export members</h2>
                </div>
                <button type="button" class="w-9 h-9 flex items-center justify-center -mr-3 group" data-action="dialog#close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" class="shrink-0 w-4 h-4 text-gray-600/70 group-hover:text-gray-700 fill-current group:text-gray-700"><title></title><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"></path></svg>
                <span class="sr-only">Close</span>
                </button>
            </div>
            <div class="mx-8 pb-3">
            <div data-controller="reload" data-reload-delay-value="1000" data-auto-refreshable-url-value="/admin/members/exports/68748">
                <div class="modal-message">
                    <p>
                    <img class="inline mr-2" src="https://assets.memberful.com/assets/admin/settings-spinner-4741fa457b5ab66d93eeda68b11ca57d97464b60401d406f31186481e5b55865.gif" />
                    Preparing your export. It will take just a minute...
                    </p>
                </div>
            </div>
            </div>
            </turbo-frame>
        """
    )

    assert parse_export_id(html_tree) == 68748


def test_parse_export_id_cancellations():
    html_tree = html.fromstring(
        """
            <turbo-frame id="modal">
            <div class="sticky top-0 bg-white flex items-start justify-between md:min-w-[460px] gap-8 border-b pb-4 pt-6 mx-8 mb-4">
                <div class="flex flex-col gap-1">
                <h2 class="text-2xl font-semibold">Export</h2>
                </div>
                <button type="button" class="w-9 h-9 flex items-center justify-center -mr-3 group" data-action="dialog#close">
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 20 20" aria-hidden="true" class="shrink-0 w-4 h-4 text-gray-600/70 group-hover:text-gray-700 fill-current group:text-gray-700"><title></title><path d="M10 8.586L2.929 1.515 1.515 2.929 8.586 10l-7.071 7.071 1.414 1.414L10 11.414l7.071 7.071 1.414-1.414L11.414 10l7.071-7.071-1.414-1.414L10 8.586z"></path></svg>
                <span class="sr-only">Close</span>
                </button>
            </div>
            <div class="mx-8 pb-3">
            <div class="mb-4" data-controller="reload" data-reload-delay-value="1000" data-auto-refreshable-url-value="/admin/csv_exports/68751">
                <div class="text-base text-gray-800">
                    <p>
                    Preparing your export. It will take just a minute...
                    </p>
                    <p class="mt-5 text-sm text-[#999]">
                    <img class="float-left mr-2.5" src="https://assets.memberful.com/assets/admin/settings-spinner-4741fa457b5ab66d93eeda68b11ca57d97464b60401d406f31186481e5b55865.gif" />
                    0 / 24
                    </p>
                </div>
            </div>
            </div>
            </turbo-frame>
        """
    )

    assert parse_export_id(html_tree) == 68751
