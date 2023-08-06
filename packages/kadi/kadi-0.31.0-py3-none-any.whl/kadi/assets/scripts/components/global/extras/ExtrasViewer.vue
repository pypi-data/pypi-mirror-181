<!-- Copyright 2020 Karlsruhe Institute of Technology
   -
   - Licensed under the Apache License, Version 2.0 (the "License");
   - you may not use this file except in compliance with the License.
   - You may obtain a copy of the License at
   -
   -     http://www.apache.org/licenses/LICENSE-2.0
   -
   - Unless required by applicable law or agreed to in writing, software
   - distributed under the License is distributed on an "AS IS" BASIS,
   - WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   - See the License for the specific language governing permissions and
   - limitations under the License. -->

<template>
  <div>
    <div v-if="!nestedType">
      <div class="row">
        <div class="col-md-6">
          <slot></slot>
        </div>
        <div class="col-md-6 d-md-flex justify-content-end" v-if="showCollapse && hasNestedType">
          <div class="mb-3">
            <button type="button"
                    class="btn btn-link text-muted p-0 mr-2"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, true)">
              <i class="fa-solid fa-square-minus"></i> {{ $t('Collapse all') }}
            </button>
            <button type="button"
                    class="btn btn-link text-muted p-0"
                    :disabled="isCollapsing"
                    @click.prevent="collapseExtras(extras_, false)">
              <i class="fa-solid fa-square-plus"></i> {{ $t('Expand all') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <ul class="list-group" :class="{'mb-2': depth > 0}">
      <li class="list-group-item extra py-1 pl-3 pr-0"
          :class="{'odd': depth % 2 == 1, 'nested': depth > 0}"
          v-for="(extra, index) in extras_"
          :key="extra.id">
        <div class="row align-items-center"
             :class="{'mb-1': kadi.utils.isNestedType(extra.type) && extra.value.length > 0 && !extra.isCollapsed}">
          <!-- Key. -->
          <div class="col-md-4">
            <span v-if="!kadi.utils.isNestedType(extra.type)">{{ extra.key || `(${index + 1})` }}</span>
            <collapse-item show-icon-class=""
                           hide-icon-class=""
                           :id="extra.id"
                           :is-collapsed="extra.isCollapsed"
                           @collapse="extra.isCollapsed = $event"
                           v-if="kadi.utils.isNestedType(extra.type)">
              <strong>{{ extra.key || `(${index + 1})` }}</strong>
            </collapse-item>
          </div>
          <!-- Value and unit. -->
          <div class="col-md-5">
            <div v-if="!kadi.utils.isNestedType(extra.type)">
              <span v-if="extra.value === null">
                <em>null</em>
              </span>
              <span v-else>
                <span v-if="extra.type !== 'date'">{{ extra.value }}</span>
                <local-timestamp :timestamp="extra.value" v-else></local-timestamp>
              </span>
              <span class="text-muted">{{ extra.unit }}</span>
            </div>
            <collapse-item show-icon-class=""
                           hide-icon-class=""
                           :id="extra.id"
                           :is-collapsed="extra.isCollapsed"
                           @collapse="extra.isCollapsed = $event"
                           v-if="kadi.utils.isNestedType(extra.type) && extra.isCollapsed && extra.value.length > 0">
              <strong>{...}</strong>
            </collapse-item>
          </div>
          <!-- Type. -->
          <div class="col-md-2 d-md-flex justify-content-end">
            <small class="text-muted mr-3">
              {{ extra.type | prettyTypeName | capitalize }}
            </small>
          </div>
          <!-- Edit link and additional information toggle. -->
          <div class="col-md-1 d-md-flex justify-content-end">
            <button type="button"
                    class="float-md-right mr-3 mr-md-0"
                    :title="$t('Toggle additional information')"
                    :class="toolbarBtnClasses"
                    @click="extra.showDetails = !extra.showDetails"
                    v-if="extra.term || extra.validation">
              <i class="fa-solid fa-angle-up" v-if="extra.showDetails"></i>
              <i class="fa-solid fa-angle-down" v-else></i>
              <span class="d-md-none">{{ $t('Toggle additional information') }}</span>
              <br>
            </button>
            <a :title="$t('Edit extra')"
               :class="toolbarBtnClasses"
               :href="getEditLink(extra, index)"
               v-if="editEndpoint">
              <i class="fa-solid fa-pencil"></i>
              <span class="d-md-none">{{ $t('Edit extra') }}</span>
            </a>
          </div>
        </div>
        <div v-if="extra.showDetails">
          <div class="card card-body bg-light text-muted py-1 px-2 my-1 mr-2">
            <div class="row my-2 my-sm-0" v-if="extra.term">
              <small class="col-sm-4">{{ $t('Term IRI') }}</small>
              <small class="col-sm-8">
                <a class="text-muted" target="_blank" rel="noopener noreferrer" :href="extra.term">
                  <i class="fa-solid fa-arrow-up-right-from-square mr-1"></i>
                  <strong>{{ extra.term }}</strong>
                </a>
              </small>
            </div>
            <div v-if="extra.validation">
              <hr class="my-1" v-if="extra.term">
              <div class="row my-2 my-sm-0" v-for="(value, key) in extra.validation" :key="key">
                <small class="col-sm-4">{{ $t('Validation') }} ({{ validationKeys[key] || key }})</small>
                <small class="col-sm-8">{{ value }}</small>
              </div>
            </div>
          </div>
        </div>
        <div v-if="kadi.utils.isNestedType(extra.type) && extra.value.length > 0">
          <div :id="extra.id" class="collapse show">
            <extras-viewer :extras="extra.value"
                           :edit-endpoint="editEndpoint"
                           :nested-type="extra.type"
                           :nested-keys="[...nestedKeys, extra.key || index]"
                           :depth="depth + 1">
            </extras-viewer>
          </div>
        </div>
      </li>
    </ul>
  </div>
</template>

<style lang="scss" scoped>
.extra {
  margin-right: -1px;

  &.odd {
    background-color: #f2f2f2;
  }

  &.nested {
    border-bottom-right-radius: 0;
    border-top-right-radius: 0;
  }
}

.text-toolbar {
  color: lighten(#95a5a6, 15%);
}
</style>

<script>
export default {
  data() {
    return {
      extras_: this.extras,
      isCollapsing: false,
      validationKeys: {
        required: $t('Required'),
        options: $t('Options'),
        range: $t('Range'),
      },
    };
  },
  props: {
    extras: Array,
    editEndpoint: {
      type: String,
      default: null,
    },
    editParam: {
      type: String,
      default: 'key',
    },
    showCollapse: {
      type: Boolean,
      default: true,
    },
    // Can also be used to detect whether we are in a nested context at all.
    nestedType: {
      type: String,
      default: null,
    },
    nestedKeys: {
      type: Array,
      default: () => [],
    },
    depth: {
      type: Number,
      default: 0,
    },
  },
  computed: {
    toolbarBtnClasses() {
      return 'btn btn-sm text-toolbar py-0 px-0 px-md-2 mr-1';
    },
    hasNestedType() {
      for (const extra of this.extras_) {
        if (kadi.utils.isNestedType(extra.type)) {
          return true;
        }
      }
      return false;
    },
  },
  methods: {
    visitExtras(extras, callback) {
      extras.forEach((extra) => {
        callback(extra);

        if (kadi.utils.isNestedType(extra.type)) {
          this.visitExtras(extra.value, callback);
        }
      });
    },
    collapseExtras(extras, collapse) {
      this.isCollapsing = true;
      this.visitExtras(extras, (extra) => extra.isCollapsed = collapse);
      // Take the collapse cooldown into account.
      window.setTimeout(() => this.isCollapsing = false, 400);
    },
    getEditLink(extra, index) {
      const url = new URL(this.editEndpoint);
      const params = new URLSearchParams(url.search);

      for (const key of this.nestedKeys) {
        params.append(this.editParam, key);
      }
      params.append(this.editParam, extra.key || index);

      url.search = params;
      return url.toString();
    },
  },
  created() {
    this.visitExtras(this.extras_, (extra) => {
      extra.id = kadi.utils.randomAlnum();
      this.$set(extra, 'showDetails', false);
      this.$set(extra, 'isCollapsed', false);
    });
  },
};
</script>
