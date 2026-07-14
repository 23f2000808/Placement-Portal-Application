<template>
  <div class="container mt-4">

    <h2 class="mb-4">
      Monthly Reports
    </h2>

    <table
      class="table table-bordered table-hover"
    >

      <thead class="table-dark">

        <tr>

          <th>Report</th>

          <th>Size (KB)</th>

          <th>Generated</th>

          <th>Action</th>

        </tr>

      </thead>

      <tbody>

        <tr
          v-for="report in reports"
          :key="report.filename"
        >

          <td>

            {{ report.filename }}

          </td>

          <td>

            {{ report.size }}

          </td>

          <td>

            {{ report.created_at }}

          </td>

          <td>

            <button
              class="btn btn-success btn-sm"
              @click="download(report.filename)"
            >

              Download

            </button>

          </td>

        </tr>

      </tbody>

    </table>

  </div>
</template>

<script>
import api from "../services/api";

export default {

  name: "ReportsView",

  data() {

    return {

      reports: []

    };

  },

  async mounted() {

    const res = await api.get(
      "/admin/reports"
    );

    this.reports = res.data;

  },

  methods: {

    download(filename) {

      window.open(

        `http://localhost:5000/api/admin/reports/${filename}`,

        "_blank"

      );

    }

  }

};
</script>
