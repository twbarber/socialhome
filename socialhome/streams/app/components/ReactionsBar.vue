<template>
    <div class="grid-item-bar d-flex justify-content-start">
        <slot />
        <div class="ml-auto grid-item-reactions mt-1">
            <b-button
                v-if="showShares"
                :class="{'item-reaction-shared': hasShared$}"
                class="item-reaction"
                @click.stop.prevent="expandShares"
            >
                <i class="fa fa-refresh" title="Shares" aria-label="Shares"></i>
                <span class="item-reaction-counter">{{ sharesCount$ }}</span>
            </b-button>
            <b-button v-if="showReplies" class="item-reaction" @click.stop.prevent="expandComments">
                <span class="item-open-replies-action">
                    <i class="fa fa-envelope" title="Replies" aria-label="Replies"></i>
                    <span class="item-reaction-counter">{{ repliesCount$ }}</span>
                </span>
            </b-button>
        </div>
        <div v-if="showSharesBox" class="content-actions">
            <b-button v-if="hasShared$" variant="secondary" @click.prevent.stop="unshare">Unshare</b-button>
            <b-button v-if="!hasShared$" variant="secondary" @click.prevent.stop="share">Share</b-button>
        </div>
        <div class="replies-container"></div>
        <div v-if="showRepliesBox">
            <div v-if="$store.state.isUserAuthenticated" class="content-actions">
                <b-button :href="replyUrl" variant="secondary">Reply</b-button>
            </div>
        </div>
    </div>
</template>

<script>
import Vue from "vue"
import store from "streams/app/stores/applicationStore"


export default Vue.component("reactions-bar", {
    store,
    props: {
        id: {type: Number, required: true},
        repliesCount: {type: Number, required: true},
        sharesCount: {type: Number, required: true},
        hasShared: {type: Boolean, required: true},
    },
    data() {
        return {
            showSharesBox: false,
            showRepliesBox: false,
            sharesCount$: this.sharesCount,
            repliesCount$: this.repliesCount,
            hasShared$: this.hasShared,
        }
    },
    computed: {
        showReplies() {
            return this.$store.state.isUserAuthenticated || this.repliesCount$ > 0
        },
        showShares() {
            return this.$store.state.isUserAuthenticated || this.sharesCount$ > 0
        },
        replyUrl() {
            return Urls["content:reply"]({pk: this.id})
        },
    },
    methods: {
        expandComments() {
            this.showRepliesBox = !this.showRepliesBox
        },
        expandShares() {
            this.showSharesBox = !this.showSharesBox
        },
        share() {
            if (!this.$store.state.isUserAuthenticated) {
                console.error("Not logged in")
                return
            }
            this.$http.post(`/api/content/${this.id}/share/`)
                .then(() => {
                    this.showSharesBox = false
                    this.sharesCount$ += 1
                    this.hasShared$ = true
                })
                .catch(err => console.error(err) /* TODO: Proper error handling */)
        },
        unshare() {
            if (!this.$store.state.isUserAuthenticated) {
                console.error("Not logged in")
                return
            }
            this.$http.delete(`/api/content/${this.id}/share/`)
                .then(() => {
                    this.showSharesBox = false
                    this.sharesCount$ -= 1
                    this.hasShared$ = false
                })
                .catch(err => console.error(err) /* TODO: Proper error handling */)
        },
    },
    updated() {
        Vue.redrawVueMasonry()
    },
})
</script>