<script>
export default{
    props: ['head', 'data'],
    template: '<table></table>',
    data() {
        return {
            instance: null
        }
    },
    watch: {
        data: function(newData) {
            if(this.instance) {
                this.instance.clear();
                this.instance.rows.add(newData);
                this.instance.draw();
            }
        }
    },
    ready() {
        this.instance = $(this.$el).DataTable({
            columns: this.head,
            data: this.data
        }).api()
    }
}
</script>
