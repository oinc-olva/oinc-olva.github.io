<template>
    <section id="instagramFeed" v-if="instagramPosts" aria-labelledby="instagramFeedTitle">
        <transition name="modalFade">
            <InstagramPostModal v-if="isPostOpened" :instagramName="instagramName" :post="currentPost" @close="closeModal" @gotoPrev="modalGotoPrev" @gotoNext="modalGotoNext" />
        </transition>
        <div id="instagramFeedContent" ref="instagramFeedContent">
            <div class="container">
                <div id="instagramFeedMeta">
                    <fa class="h2Icon" :icon="['fab', 'instagram']" />
                    <h2 id="instagramFeedTitle">Vind ons op Instagram</h2>
                    <a id="instagramFeedFollow" class="btn" :href="`https://instagram.com/${this.instagramName}`" target="_blank">Volg <span>@{{this.instagramName}}</span></a>
                </div>
                <ul id="instagramFeedGallery" ref="instagramFeedGallery" aria-label="Instagram posts">
                    <li v-for="(post, i) in instagramPosts.slice(0, shownPostCount)" :key="post">
                        <InstagramPostPreview :post="post" @open="openPost(post, i)" />
                    </li>
                </ul>
                <button id="instagramFeedShowMore" class="btn" @click="showMorePosts()" v-if="shownPostCount < instagramPosts.length">Meer laden</button>
            </div>
        </div>
        <div id="instagramFeedBottom">
            <svg data-name="Layer 1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 120" preserveAspectRatio="none">
                <path d="M0,0V46.29c47.79,22.2,103.59,32.17,158,28,70.36-5.37,136.33-33.31,206.8-37.5C438.64,32.43,512.34,53.67,583,72.05c69.27,18,138.3,24.88,209.4,13.08,36.15-6,69.85-17.84,104.45-29.34C989.49,25,1113-14.29,1200,52.47V0Z" opacity=".25" class="shape-fill"></path>
                <path d="M0,0V15.81C13,36.92,27.64,56.86,47.69,72.05,99.41,111.27,165,111,224.58,91.58c31.15-10.15,60.09-26.07,89.67-39.8,40.92-19,84.73-46,130.83-49.67,36.26-2.85,70.9,9.42,98.6,31.56,31.77,25.39,62.32,62,103.63,73,40.44,10.79,81.35-6.69,119.13-24.28s75.16-39,116.92-43.05c59.73-5.85,113.28,22.88,168.9,38.84,30.2,8.66,59,6.17,87.09-7.5,22.43-10.89,48-26.93,60.65-49.24V0Z" opacity=".5" class="shape-fill"></path>
                <path d="M0,0V5.63C149.93,59,314.09,71.32,475.83,42.57c43-7.64,84.23-20.12,127.61-26.46,59-8.63,112.48,12.24,165.56,35.4C827.93,77.22,886,95.24,951.2,90c86.53-7,172.46-45.71,248.8-84.81V0Z" class="shape-fill"></path>
            </svg>
        </div>
    </section>
</template>

<script>
import InstagramPostModal from '../components/InstagramPostModal.vue'
import InstagramPostPreview from '../components/InstagramPostPreview.vue'

export default {
    name: 'InstagramFeed',
    components: {
        InstagramPostModal,
        InstagramPostPreview
    },
    data() {
        return {
            instagramPosts: null,
            instagramName: '',
            shownPostCount: 6,
            isPostOpened: false,
            currentPost: null,
            currentPostIndex: 0
        }
    },
    methods: {
        async fetchInstagramData() {
            const res = await fetch('/generated/data/instagram.json')
            const data = await res.json()
            return data
        },
        findPostDataFromId(postId) {
            for (let i = 0; i < this.instagramPosts.length; i++)
                if (this.instagramPosts[i].id == postId) return this.instagramPosts[i]
        },
        showMorePosts() {
            this.shownPostCount += 5;
            this.$nextTick(() => {
                this.$refs.instagramFeedGallery.getElementsByClassName('instagramPostPreviewWrapper')[this.shownPostCount - 5].focus();
            })
        },
        openPost(post, postIndex) {
            this.currentPost = post;
            this.currentPostIndex = postIndex;
            this.isPostOpened = true;
            this.$router.push({
                path: '/',
                query: {
                    instagram_post: post.id
                }
            })
        },
        closeModal() {
            this.isPostOpened = false;
            this.$router.push({
                path: '/'
            })
        },
        modalGotoPrev() {
            let newPostIndex = this.currentPostIndex - 1;
            if (newPostIndex < 0) newPostIndex = this.instagramPosts.length - 1;
            this.openPost(this.instagramPosts[newPostIndex], newPostIndex);
        },
        modalGotoNext() {
            let newPostIndex = this.currentPostIndex + 1;
            if (newPostIndex == this.instagramPosts.length) newPostIndex = 0;
            this.openPost(this.instagramPosts[newPostIndex], newPostIndex);
        }
    },
    async mounted() {
        let instagramData = await this.fetchInstagramData();
        this.instagramPosts = instagramData.posts;
        this.instagramName = instagramData.username;

        this.currentPost = this.findPostDataFromId(this.$route.query.instagram_post);
        if (this.currentPost) {
            this.isPostOpened = true;
            this.$nextTick(() => {
                this.$refs.instagramFeedContent.scrollIntoView({ behavior: 'smooth' });
            })
        }
    }
}
</script>

<style lang="scss" scoped>
    #instagramFeed {
        position: relative;
    }
    #instagramFeedContent {
        background: $sectionBackgroundDark;
        padding: calc(4vw + 30px) 0;
    }
    #instagramFeedMeta {
        display: flex;
        align-items: center;

        h2 {
            display: inline-block;
            font-size: 2.5em;
            flex: 1;
            align-content: center;
        }
        a {
            margin-left: 100px;

            span {
                margin-left: 5px;
                color: rgb(183, 201, 228);
            }
        }
    }
    #instagramFeedGallery {
        display: grid;
        grid-template-columns: repeat( auto-fill, minmax(calc(140px + 7%), 1fr) );
        padding: 50px calc(5px + 3%);

        li {
            display: inline-block;
            list-style: none;
        }
    }
    #instagramFeedShowMore {
        display: block;
        margin: auto;
    }
    #instagramFeedBottom {
        position: absolute;
        left: 0;
        bottom: 0;
        width: 100%;
        overflow: hidden;
        line-height: 0;
        transform: rotate(180deg);

        svg {
            position: relative;
            display: block;
            width: calc(100% + 1.3px);
            height: 34px;
        }
        .shape-fill { fill: $sectionBackgroundLight; }
    }
    
    @media screen and (max-width: 920px) {
        #instagramFeedMeta {
            flex-direction: column;

            svg { display: none; }
            h2 {
                margin: 20px 0 40px;
                text-align: center;
                font-size: calc(2vw + 20px);
            }
            svg, a { margin: 0; }
        }
    }
</style>