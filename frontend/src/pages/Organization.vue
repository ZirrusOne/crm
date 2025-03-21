<template>
  <LayoutHeader v-if="organization.doc">
    <template #left-header>
      <Breadcrumbs :items="breadcrumbs">
        <template #prefix="{ item }">
          <Icon v-if="item.icon" :icon="item.icon" class="mr-2 h-4" />
        </template>
      </Breadcrumbs>
    </template>
  </LayoutHeader>
  <div v-if="organization.doc" class="flex flex-1 flex-col overflow-hidden">
    <FileUploader
      @success="changeOrganizationImage"
      :validateFile="validateFile"
    >
      <template #default="{ openFileSelector, error }">
        <div class="flex items-start justify-start gap-6 p-5 sm:items-center">
          <div class="group relative h-24 w-24">
            <Avatar
              size="3xl"
              :image="organization.doc.organization_logo"
              :label="organization.doc.name"
              class="!h-24 !w-24"
            />
            <component
              :is="organization.doc.organization_logo ? Dropdown : 'div'"
              v-bind="
                organization.doc.organization_logo
                  ? {
                      options: [
                        {
                          icon: 'upload',
                          label: organization.doc.organization_logo
                            ? __('Change image')
                            : __('Upload image'),
                          onClick: openFileSelector,
                        },
                        {
                          icon: 'trash-2',
                          label: __('Remove image'),
                          onClick: () => changeOrganizationImage(''),
                        },
                      ],
                    }
                  : { onClick: openFileSelector }
              "
              class="!absolute bottom-0 left-0 right-0"
            >
              <div
                class="z-1 absolute bottom-0 left-0 right-0 flex h-13 cursor-pointer items-center justify-center rounded-b-full bg-black bg-opacity-40 pt-3 opacity-0 duration-300 ease-in-out group-hover:opacity-100"
                style="
                  -webkit-clip-path: inset(12px 0 0 0);
                  clip-path: inset(12px 0 0 0);
                "
              >
                <CameraIcon class="h-6 w-6 cursor-pointer text-white" />
              </div>
            </component>
          </div>
          <div class="flex flex-col justify-center gap-2 sm:gap-0.5">
            <div class="text-3xl font-semibold text-gray-900">
              {{ organization.doc.name }}
            </div>
            <div
              class="flex flex-col flex-wrap gap-3 text-base text-gray-700 sm:flex-row sm:items-center sm:gap-2"
            >
            <div class="flex items-center gap-2" v-if="organization.doc.is_partner == 1">
              <PartnerIcon class="h-4 w-4" />
                  <div>Partner</div>
            </div>
              
              <Tooltip text="Website">
                <div
                  v-if="organization.doc.website"
                  class="flex items-center gap-1.5"
                >
                  <WebsiteIcon class="h-4 w-4" />
                  <span class="">{{ website(organization.doc.website) }}</span>
                </div>
              </Tooltip>
              <span
                v-if="organization.doc.website"
                class="hidden text-3xl leading-[0] text-gray-600 sm:flex"
              >
                &middot;
              </span>
              <Tooltip text="Government Affiliation">
                <div
                  v-if="organization.doc.government_affiliation"
                  class="flex items-center gap-1.5"
                >
                  <FeatherIcon name="crosshair" class="h-4 w-4" />
                  <span class="">{{ organization.doc.government_affiliation }}</span>
                </div>
              </Tooltip>
              <span
                v-if="organization.doc.government_affiliation"
                class="hidden text-3xl leading-[0] text-gray-600 sm:flex"
              >
                &middot;
              </span>
              <Tooltip text="Industry">
                <div
                  v-if="organization.doc.industry"
                  class="flex items-center gap-1.5"
                >
                  <FeatherIcon name="briefcase" class="h-4 w-4" />
                  <span class="">{{ organization.doc.industry }}</span>
                </div>
              </Tooltip>
              <span
                v-if="organization.doc.industry"
                class="hidden text-3xl leading-[0] text-gray-600 sm:flex"
              >
                &middot;
              </span>
              <Tooltip text="Territory">
                <div
                  v-if="organization.doc.territory"
                  class="flex items-center gap-1.5"
                >
                  <TerritoryIcon class="h-4 w-4" />
                  <span class="">{{ organization.doc.territory }}</span>
                </div>
              </Tooltip>
              <div
                v-if="organization.doc.territory"
                class="flex items-center gap-1.5"
              >
                <TerritoryIcon class="h-4 w-4" />
                <span class="">{{ organization.doc.territory }}</span>
              </div>
              <span
                v-if="organization.doc.territory"
                class="hidden text-3xl leading-[0] text-gray-600 sm:flex"
              >
                &middot;
              </span>
              <Tooltip text="Annual Revenue">
                <div
                  v-if="organization.doc.annual_revenue"
                  class="flex items-center gap-1.5"
                >
                  <MoneyIcon class="size-4" />
                  <span class="">{{
                    customFormatNumberIntoCurrency(
                      organization.doc.annual_revenue,
                      organization.doc.currency,
                    )
                  }}</span>
                </div>
              </Tooltip>
              <span
                v-if="organization.doc.annual_revenue"
                class="hidden text-3xl leading-[0] text-gray-600 sm:flex"
              >
                &middot;
              </span>
              <Button
                v-if="
                  organization.doc.website ||
                  organization.doc.industry ||
                  organization.doc.territory ||
                  organization.doc.annual_revenue
                "
                variant="ghost"
                :label="__('More')"
                class="w-fit cursor-pointer hover:text-gray-900 sm:-ml-1"
                @click="
                  () => {
                    detailMode = true
                    showOrganizationModal = true
                  }
                "
              />
            </div>
            <div class="mt-2 flex gap-1.5">
              <Button
                :label="__('Edit')"
                size="sm"
                @click="
                  () => {
                    detailMode = false
                    showOrganizationModal = true
                  }
                "
              >
                <template #prefix>
                  <EditIcon class="h-4 w-4" />
                </template>
              </Button>
              <Button
                :label="__('Delete')"
                theme="red"
                size="sm"
                @click="deleteOrganization"
              >
                <template #prefix>
                  <FeatherIcon name="trash-2" class="h-4 w-4" />
                </template>
              </Button>
            </div>
            <ErrorMessage class="mt-2" :message="__(error)" />
          </div>
        </div>
      </template>
    </FileUploader>
    <Tabs v-model="tabIndex" :tabs="tabs">
      <template #tab="{ tab, selected }">
        <button
          class="group flex items-center gap-2 border-b border-transparent py-2.5 text-base text-gray-600 duration-300 ease-in-out hover:border-gray-400 hover:text-gray-900"
          :class="{ 'text-gray-900': selected }"
        >
          <component v-if="tab.icon" :is="tab.icon" class="h-5" />
          {{ __(tab.label) }}
          <Badge
            class="group-hover:bg-gray-900"
            :class="[selected ? 'bg-gray-900' : 'bg-gray-600']"
            variant="solid"
            theme="gray"
            size="sm"
          >
            {{ tab.count }}
          </Badge>
        </button>
      </template>
      <template #default="{ tab }">
        <DealsListView
          class="mt-4"
          v-if="tab.label === 'Deals' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: true }"
        />
        <ContactsListView
          class="mt-4"
          v-if="tab.label === 'Contacts' && rows.length"
          :rows="rows"
          :columns="columns"
          :options="{ selectable: false, showTooltip: true }"
        />
        <div
          v-if="!rows.length"
          class="grid flex-1 place-items-center text-xl font-medium text-gray-500"
        >
          <div class="flex flex-col items-center justify-center space-y-3">
            <component :is="tab.icon" class="!h-10 !w-10" />
            <div>{{ __('No {0} Found', [__(tab.label)]) }}</div>
          </div>
        </div>
      </template>
    </Tabs>
  </div>
  <OrganizationModal
    v-model="showOrganizationModal"
    v-model:quickEntry="showQuickEntryModal"
    v-model:organization="organization"
    :options="{ detailMode }"
  />
  <QuickEntryModal
    v-if="showQuickEntryModal"
    v-model="showQuickEntryModal"
    doctype="CRM Organization"
  />
</template>

<script setup>
import Icon from '@/components/Icon.vue'
import LayoutHeader from '@/components/LayoutHeader.vue'
import OrganizationModal from '@/components/Modals/OrganizationModal.vue'
import QuickEntryModal from '@/components/Modals/QuickEntryModal.vue'
import DealsListView from '@/components/ListViews/DealsListView.vue'
import ContactsListView from '@/components/ListViews/ContactsListView.vue'
import WebsiteIcon from '@/components/Icons/WebsiteIcon.vue'
import TerritoryIcon from '@/components/Icons/TerritoryIcon.vue'
import MoneyIcon from '@/components/Icons/MoneyIcon.vue'
import EditIcon from '@/components/Icons/EditIcon.vue'
import CameraIcon from '@/components/Icons/CameraIcon.vue'
import DealsIcon from '@/components/Icons/DealsIcon.vue'
import ContactsIcon from '@/components/Icons/ContactsIcon.vue'
import { globalStore } from '@/stores/global'
import { usersStore } from '@/stores/users'
import { statusesStore } from '@/stores/statuses'
import { getView } from '@/utils/view'
import {
  dateFormat,
  dateTooltipFormat,
  timeAgo,
  customFormatNumberIntoCurrency,
} from '@/utils'
import {
  Breadcrumbs,
  Avatar,
  FileUploader,
  Dropdown,
  Tabs,
  Tooltip,
  call,
  createListResource,
  createDocumentResource,
  usePageMeta,
} from 'frappe-ui'
import { h, computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import PartnerIcon from '@/components/Icons/PartnerIcon.vue'


const props = defineProps({
  organizationId: {
    type: String,
    required: true,
  },
})

const { $dialog } = globalStore()
const { getDealStatus } = statusesStore()
const showOrganizationModal = ref(false)
const showQuickEntryModal = ref(false)
const detailMode = ref(false)

const route = useRoute()
const router = useRouter()

const organization = createDocumentResource({
  doctype: 'CRM Organization',
  name: props.organizationId,
  cache: ['organization', props.organizationId],
  fields: ['*'],
  auto: true,
})

const breadcrumbs = computed(() => {
  let items = [{ label: __('Organizations'), route: { name: 'Organizations' } }]

  if (route.query.view || route.query.viewType) {
    let view = getView(
      route.query.view,
      route.query.viewType,
      'CRM Organization',
    )
    if (view) {
      items.push({
        label: __(view.label),
        icon: view.icon,
        route: {
          name: 'Organizations',
          params: { viewType: route.query.viewType },
          query: { view: route.query.view },
        },
      })
    }
  }

  items.push({
    label: props.organizationId,
    route: {
      name: 'Organization',
      params: { organizationId: props.organizationId },
    },
  })
  return items
})

usePageMeta(() => {
  return {
    title: props.organizationId,
  }
})

function validateFile(file) {
  let extn = file.name.split('.').pop().toLowerCase()
  if (!['png', 'jpg', 'jpeg'].includes(extn)) {
    return __('Only PNG and JPG images are allowed')
  }
}

async function changeOrganizationImage(file) {
  await call('frappe.client.set_value', {
    doctype: 'CRM Organization',
    name: props.organizationId,
    fieldname: 'organization_logo',
    value: file?.file_url || '',
  })
  organization.reload()
}

async function deleteOrganization() {
  $dialog({
    title: __('Delete organization'),
    message: __('Are you sure you want to delete this organization?'),
    actions: [
      {
        label: __('Delete'),
        theme: 'red',
        variant: 'solid',
        async onClick(close) {
          await call('frappe.client.delete', {
            doctype: 'CRM Organization',
            name: props.organizationId,
          })
          close()
          router.push({ name: 'Organizations' })
        },
      },
    ],
  })
}

function website(url) {
  return url && url.replace(/^(?:https?:\/\/)?(?:www\.)?/i, '')
}

const tabIndex = ref(0)
const tabs = [
  {
    label: 'Deals',
    icon: h(DealsIcon, { class: 'h-4 w-4' }),
    count: computed(() => deals.data?.length),
  },
  {
    label: 'Contacts',
    icon: h(ContactsIcon, { class: 'h-4 w-4' }),
    count: computed(() => contacts.data?.length),
  },
]

const { getUser } = usersStore()

const deals = createListResource({
  type: 'list',
  doctype: 'CRM Deal',
  cache: ['deals', props.organizationId],
  fields: [
    'name',
    'organization',
    'currency',
    'annual_revenue',
    'status',
    'email',
    'mobile_no',
    'deal_owner',
    'modified',
  ],
  filters: {
    organization: props.organizationId,
  },
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true,
})

const contacts = createListResource({
  type: 'list',
  doctype: 'Contact',
  cache: ['contacts', props.organizationId],
  fields: [
    'name',
    'full_name',
    'image',
    'email_id',
    'mobile_no',
    'company_name',
    'modified',
  ],
  filters: {
    company_name: props.organizationId,
  },
  orderBy: 'modified desc',
  pageLength: 20,
  auto: true,
})

const rows = computed(() => {
  let list = []
  list = !tabIndex.value ? deals : contacts

  if (!list.data) return []

  return list.data.map((row) => {
    return !tabIndex.value ? getDealRowObject(row) : getContactRowObject(row)
  })
})

const columns = computed(() => {
  return tabIndex.value === 0 ? dealColumns : contactColumns
})

function getDealRowObject(deal) {
  return {
    name: deal.name,
    organization: {
      label: deal.organization,
      logo: props.organization?.organization_logo,
    },
    annual_revenue: customFormatNumberIntoCurrency(
      deal.annual_revenue,
      deal.currency,
    ),
    status: {
      label: deal.status,
      color: getDealStatus(deal.status)?.iconColorClass,
    },
    email: deal.email,
    mobile_no: deal.mobile_no,
    deal_owner: {
      label: deal.deal_owner && getUser(deal.deal_owner).full_name,
      ...(deal.deal_owner && getUser(deal.deal_owner)),
    },
    modified: {
      label: dateFormat(deal.modified, dateTooltipFormat),
      timeAgo: __(timeAgo(deal.modified)),
    },
  }
}

function getContactRowObject(contact) {
  return {
    name: contact.name,
    full_name: {
      label: contact.full_name,
      image_label: contact.full_name,
      image: contact.image,
    },
    email: contact.email_id,
    mobile_no: contact.mobile_no,
    company_name: {
      label: contact.company_name,
      logo: props.organization?.organization_logo,
    },
    modified: {
      label: dateFormat(contact.modified, dateTooltipFormat),
      timeAgo: __(timeAgo(contact.modified)),
    },
  }
}

const dealColumns = [
  {
    label: __('Organization'),
    key: 'organization',
    width: '11rem',
  },
  {
    label: __('Amount'),
    key: 'annual_revenue',
    width: '9rem',
  },
  {
    label: __('Status'),
    key: 'status',
    width: '10rem',
  },
  {
    label: __('Email'),
    key: 'email',
    width: '12rem',
  },
  {
    label: __('Mobile no'),
    key: 'mobile_no',
    width: '11rem',
  },
  {
    label: __('Deal owner'),
    key: 'deal_owner',
    width: '10rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]

const contactColumns = [
  {
    label: __('Name'),
    key: 'full_name',
    width: '17rem',
  },
  {
    label: __('Email'),
    key: 'email',
    width: '12rem',
  },
  {
    label: __('Phone'),
    key: 'mobile_no',
    width: '12rem',
  },
  {
    label: __('Organization'),
    key: 'company_name',
    width: '12rem',
  },
  {
    label: __('Last modified'),
    key: 'modified',
    width: '8rem',
  },
]
</script>
