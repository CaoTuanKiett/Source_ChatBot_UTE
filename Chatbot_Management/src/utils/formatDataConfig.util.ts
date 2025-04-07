type DataConfigFormat = {
    dataFile: any[]
    dataImportFile: any[]
    dataLink: any[]
    dataQA: any[]
}

function formatDataConfig(dataConfig: DataConfigFormat) {
    const dataCheck: DataConfigFormat = {
        dataFile: dataConfig?.dataFile ? Array.from(dataConfig?.dataFile) : [],
        dataImportFile: dataConfig?.dataImportFile
            ? Array.from(dataConfig?.dataImportFile).map((item: any) => {
                  const newItem = Object.assign({}, item)
                  if (newItem.originFileObj && typeof newItem.originFileObj === 'object') {
                      newItem.originFileObj = { ...newItem.originFileObj }
                  }

                  return newItem
              })
            : [],
        dataLink: dataConfig?.dataLink ? Array.from(dataConfig?.dataLink) : [],
        dataQA: dataConfig?.dataQA
            ? Array.from(dataConfig?.dataQA).map((item: any) => {
                  return Object.assign({}, item)
              })
            : []
    }

    return dataCheck
}

export default formatDataConfig
