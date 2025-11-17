/* Shared utils */
function getSchemaDataFields(schema) {
  let dataFields = []
  if (schema) {
    let extra_fields = Object.keys(schema.properties)
    dataFields = [...dataFields, ...extra_fields];
    dataFields = [...new Set(dataFields)]
  }
  return dataFields
}

export {getSchemaDataFields}
