<template>
  <div>
    <h5 v-html="this.title"></h5>
    <b-tabs>
      <b-tab title="notes" active>
        <div class="overflow-auto">
            <b-table
              id="my-notes"
              :items="notes"
              :per-page="perPage"
              :current-page="currentPage"
              :fields='fields'
              small
            >
              &nbsp;<template v-slot:cell(title)="data">
                <div><a href="#" @click="editNote(data.item)">{{ data.item.title }}</a></div>
                <tag :parent_folder="Object.assign({}, data.item.tag)"/>
                <div class="text-sm text-muted font-italic" style="font-size: 0.7rem">Created: {{ moment(data.item.created_time).format('llll') }} - Updated: {{ moment(data.item.updated_time).format('llll') }}</div>
              </template>
            </b-table>
            <b-pagination
              v-model="currentPage"
              :total-rows="notes.length"
              :per-page="perPage"
              aria-controls="my-notes"
            ></b-pagination>
          </div>
      </b-tab>
      <b-tab title="tasks">
        <div class="overflow-auto">
            <b-table
              id="my-tasks"
              :items="tasks"
              :per-page="perPage"
              :current-page="currentPageTasks"
              :fields='fields'
              :tbody-tr-class='rowClass'
              small
            >
              &nbsp;<template v-slot:cell(title)="data">
                <div><a href="#" @click="editNote(data.item)">{{ data.item.title }}</a></div>
                <tag :parent_folder="Object.assign({}, data.item.tag)"/>
                <div v-if="data.item.todo_completed > 0" class="text-sm text-muted font-italic" style="font-size: 0.7rem">Completed: {{ moment(data.item.completed).format('llll') }}</div>
                <div v-if="data.item.todo_due > 0" class="text-sm text-muted font-italic" style="font-size: 0.7rem">Due: {{ moment(data.item.todo_due).format('llll') }}</div>
                <div class="text-sm text-muted font-italic" style="font-size: 0.7rem">Created: {{ moment(data.item.created_time).format('llll') }} - Updated: {{ moment(data.item.updated_time).format('llll') }}</div>
              </template>
            </b-table>
            <b-pagination
              v-model="currentPageTasks"
              :total-rows="tasks.length"
              :per-page="perPage"
              aria-controls="my-tasks"
            ></b-pagination>
          </div>
      </b-tab>
    </b-tabs>
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
import { createHelpers } from 'vuex-map-fields'
import getters from '../getters'
import actions from '../actions'
import types from '../types'

import Tag from './Tag'

const namespace = 'notes'
const { mapGetters, mapActions } = createNamespacedHelpers(namespace)

const { mapFields } = createHelpers({
  getterType: 'getNoteField',
  mutationType: 'updateNoteField'
})

export default {
  data () {
    return {
      page: 0,
      currentPage: 1,
      currentPageTasks: 1,
      perPage: 20,
      fields: [
        { key: 'title', label: 'Note', sortable: true }
      ]
    }
  },
  components: { Tag },
  methods: {
    editNote (note) {
      this.$store.dispatch('notes/' + types.NOTETAG_SET, note)
      this.$store.dispatch('notes/' + types.NOTE_SET, note)
    },
    delNote (id) {
      this.$store.dispatch('notes/' + types.NOTE_REMOVE, id)
    },
    ...mapActions(Object.keys(actions)),
    rowClass (item, type) {
      if (!item) return
      if (item.todo_completed > 0) return 'table-secondary'
    }
  },
  computed: {
    ...mapGetters(Object.keys(getters)),
    title: {
      get () {
        if (this.$store.state.folders.folder.title !== undefined) {
          return '<i class="fas fa-folder-open"></i> From Folder / ' + this.$store.state.folders.folder.title
        } else if (this.$store.state.tags.tag.title !== undefined) {
          return '<i class="fas fa-tags"></i> From Tag / ' + this.$store.state.tags.tag.title
        }
        return 'All notes'
      }
    },
    /* only get notes that are not "tasks" */
    notes () {
      return this.$store.state.notes.notes.filter(note => note.is_todo === 0)
    },
    /* only get the tasks */
    tasks () {
      return this.$store.state.notes.notes.filter(note => note.is_todo === 1)
    },
    ...mapFields('notes', {
      id: 'note.id',
      is_todo: 'note.is_todo',
      parent_id: 'note.parent_id',
      created_time: 'note.user_created_time',
      updated_time: 'note.updated_time',
      todo_completed: 'note.todo_completed',
      todo_due: 'note.todo_due',
      author: 'note.author',
      tag: 'tag'
    })
  },
  mounted () {
    this.$store.dispatch('notes/' + types.NOTE_FETCH_ALL)
  }
}
</script>
