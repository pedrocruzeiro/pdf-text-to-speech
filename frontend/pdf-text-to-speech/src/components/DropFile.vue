
<template>
  <div class="container">
    <div>
      <h2>Single File</h2>
      <hr/>
      <label>File
        <input type="file" @change="handleFileUpload( $event )"/>
      </label>
      <br>
      <button v-on:click="submitFile()">Submit</button>
    </div>
  </div>
</template>


<script>

import axios from 'axios'

  export default {
    data(){
        return {
            file: ''
        }
    },
    methods: {
      handleFileUpload( event ){
        this.file = event.target.files[0];
    },
    submitFile(){
        let formData = new FormData();
        formData.append('file', this.file);
        console.log(this.file)
        if(this.file['type']==='application/pdf'){
            
            axios.post( 'http://localhost:8002/pdf',
                formData,
                {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
              }
            ).then(function (response) {
                console.log(response)
    let fileName = response.headers["content-disposition"].split("filename=")[1];
    if (window.navigator && window.navigator.msSaveOrOpenBlob) { // IE variant
        window.navigator.msSaveOrOpenBlob(new Blob([response.data],
                { type: 'audio/mpeg' }
            ),
            fileName
        );
    } else {
        const url = window.URL.createObjectURL(new Blob([response.data],
            { type: 'application/pdf' }));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download',
            response.headers["content-disposition"].split("filename=")[1]);
        document.body.appendChild(link);
        link.click();
    }
    }
)
        .catch(function(){
          console.log('FAILURE!!');
        });
        }
    
      },
    }
  }
</script>