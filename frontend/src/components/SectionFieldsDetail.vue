<template>
  <FadedScrollableDiv
    class="flex flex-col gap-1.5 overflow-y-auto"
    :class="[isLastSection ? '' : 'max-h-[300px]']"
  >
    <div
    v-for="field in _fields.filter(field => ['Amount', 'Probability', 'Close Date', 'Next Step', 'Deal Owner'].includes(field.label))"
    :key="field.label"
      :class="[field.hidden && 'hidden']"
      class="section-field flex items-center gap-2 px-3 leading-5 first:mt-3"
    >
      <Tooltip :text="__(field.label)" :hoverDelay="1">
        <div class="sm:w-[106px] w-36 shrink-0 truncate text-sm text-gray-600">
          <span>{{ __(field.label) }}</span>
          <span class="text-red-500">{{ field.reqd ? ' *' : '' }}</span>
        </div>
      </Tooltip>
      <div
        class="grid min-h-[28px] flex-1 items-center overflow-hidden text-base"
      >
        <div
          v-if="field.read_only && field.type !== 'checkbox'"
          class="flex h-7 cursor-pointer items-center px-2 py-1 text-gray-600"
        >
          <Tooltip :text="__(field.tooltip)">
            <div>{{ data[field.name] }}</div>
          </Tooltip>
        </div>
        <FormControl
          v-else-if="field.type == 'checkbox'"
          class="form-control"
          :type="field.type"
          v-model="data[field.name]"
          @change.stop="emit('update', field.name, $event.target.checked)"
          :disabled="Boolean(field.read_only)"
        />
        <FormControl
          v-else-if="
            ['email', 'number', 'date', 'password', 'textarea'].includes(
              field.type,
            )
          "
          class="form-control"
          :class="{
            '[&_input]:text-gray-500':
              field.type === 'date' && !data[field.name],
          }"
          :type="field.type"
          :value="data[field.name]"
          :placeholder="field.placeholder"
          :debounce="500"
          @change.stop="emit('update', field.name, $event.target.value)"
        />
        <FormControl
          v-else-if="field.type === 'select'"
          class="form-control cursor-pointer [&_select]:cursor-pointer"
          type="select"
          v-model="data[field.name]"
          :options="field.options"
          :placeholder="field.placeholder"
          @change.stop="emit('update', field.name, $event.target.value)"
        />
        <Link
          v-else-if="['lead_owner', 'deal_owner'].includes(field.name)"
          class="form-control"
          :value="data[field.name] && getUser(data[field.name]).full_name"
          doctype="User"
          :filters="field.filters"
          @change="(data) => emit('update', field.name, data)"
          :placeholder="'Select' + ' ' + field.label + '...'"
          :hideMe="true"
        >
          <template v-if="data[field.name]" #prefix>
            <UserAvatar class="mr-1.5" :user="data[field.name]" size="sm" />
          </template>
          <template #item-prefix="{ option }">
            <UserAvatar class="mr-1.5" :user="option.value" size="sm" />
          </template>
          <template #item-label="{ option }">
            <Tooltip :text="option.value">
              <div class="cursor-pointer">
                {{ getUser(option.value).full_name }}
              </div>
            </Tooltip>
          </template>
        </Link>
        <Link
          v-else-if="field.type === 'link'"
          class="form-control select-text"
          :value="data[field.name]"
          :doctype="field.doctype"
          :filters="field.filters"
          :placeholder="field.placeholder"
          @change="(data) => emit('update', field.name, data)"
          :onCreate="field.create"
        />
        <FormControl
          v-else
          class="form-control"
          type="text"
          :value="data[field.name]"
          :placeholder="field.placeholder"
          :debounce="500"
          @change.stop="emit('update', field.name, $event.target.value)"
        />
      </div>
      <ArrowUpRightIcon
        v-if="field.type === 'link' && field.link && data[field.name]"
        class="h-4 w-4 shrink-0 cursor-pointer text-gray-600 hover:text-gray-800"
        @click="field.link(data[field.name])"
      />
    </div>
    <div
    v-if="_fields.find(f => f.label === 'Amount') && _fields.find(f => f.label === 'Probability')"
    class="section-field flex items-center gap-2 px-3 leading-5 first:mt-3"
    >
      <div data-v-45950e06="" class="sm:w-[106px] w-36 shrink-0  text-sm text-gray-600" data-state="closed">
        <span data-v-45950e06="">Weighted Amount</span>

    </div>
    <div data-v-f76baccb="" class="grid min-h-[28px] flex-1 items-center overflow-hidden text-base">
      <div data-v-f76baccb="" class="space-y-1.5 form-control"><!---->
        <div class="relative flex items-center" value="Close deal">
          {{crm_deal_weighted_amount ? customFormatNumberIntoCurrency(crm_deal_annual_revenue*(crm_deal_probability/100), 'USD') : 0}} 
        </div>
      </div>
    </div>
</div>

  </FadedScrollableDiv>
</template>

<script setup>
import FadedScrollableDiv from '@/components/FadedScrollableDiv.vue'
import ArrowUpRightIcon from '@/components/Icons/ArrowUpRightIcon.vue'
import Link from '@/components/Controls/Link.vue'
import UserAvatar from '@/components/UserAvatar.vue'
import { usersStore } from '@/stores/users'
import { Tooltip } from 'frappe-ui'
import { computed } from 'vue'

const props = defineProps({
  fields: {
    type: Object,
  },
  crm_deal_probability: {
    type: String,
  },
  crm_deal_annual_revenue: {
    type: String,
  },
  crm_deal_weighted_amount:{
    type: String,
  },
  isLastSection: {
    type: Boolean,
    default: false,
  },
})

const { getUser } = usersStore()

const emit = defineEmits(['update'])

const data = defineModel()

const _fields = computed(() => {
  let all_fields = []
  props.fields?.forEach((field) => {
    let df = field?.all_properties
    if (df?.depends_on) evaluate_depends_on(df.depends_on, field)
    all_fields.push({
      ...field,
      filters: df?.link_filters && JSON.parse(df.link_filters),
      placeholder: field.placeholder || field.label,
    })
  })
  return all_fields
})

function evaluate_depends_on(expression, field) {
  if (expression.substr(0, 5) == 'eval:') {
    try {
      let out = evaluate(expression.substr(5), { doc: data.value })
      if (!out) {
        field.hidden = true
      }
    } catch (e) {
      console.error(e)
    }
  }
}

function evaluate(code, context = {}) {
  let variable_names = Object.keys(context)
  let variables = Object.values(context)
  code = `let out = ${code}; return out`
  try {
    let expression_function = new Function(...variable_names, code)
    return expression_function(...variables)
  } catch (error) {
    console.log('Error evaluating the following expression:')
    console.error(code)
    throw error
  }
}
function customFormatNumberIntoCurrency(value, currency) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
        currency: currency
    }).format(value);
}
</script>

<style scoped>
.form-control {
  margin: 2px;
}

:deep(.form-control input:not([type='checkbox'])),
:deep(.form-control select),
:deep(.form-control textarea),
:deep(.form-control button) {
  border-color: transparent;
  background: white;
}

:deep(.form-control button) {
  gap: 0;
}
:deep(.form-control [type='checkbox']) {
  margin-left: 9px;
  cursor: pointer;
}

:deep(.form-control button > div) {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

:deep(.form-control button svg) {
  color: white;
  width: 0;
}
</style>
