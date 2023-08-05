"use strict";
(() => {
var exports = {};
exports.id = 405;
exports.ids = [405];
exports.modules = {

/***/ "@mui/material":
/***/ ((module) => {

module.exports = require("@mui/material");

/***/ }),

/***/ "react":
/***/ ((module) => {

module.exports = require("react");

/***/ }),

/***/ "react/jsx-runtime":
/***/ ((module) => {

module.exports = require("react/jsx-runtime");

/***/ }),

/***/ "process":
/***/ ((module) => {

module.exports = require("process");

/***/ }),

/***/ "(sc_server)/./pages/index.server.js":
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "__next_rsc__": () => (/* binding */ index_server_next_rsc_),
  "default": () => (/* binding */ index_server),
  "getServerSideProps": () => (/* binding */ getServerSideProps)
});

// EXTERNAL MODULE: external "react/jsx-runtime"
var jsx_runtime_ = __webpack_require__("react/jsx-runtime");
// EXTERNAL MODULE: external "react"
var external_react_ = __webpack_require__("react");
;// CONCATENATED MODULE: ./components/SettingsBar/MatrixSelect.client.js
const MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const MatrixSelect_client = ({ $$typeof: MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/SettingsBar/MatrixSelect.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Modals/DialogueModalContainer.client.js
const DialogueModalContainer_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const DialogueModalContainer_client = ({ $$typeof: DialogueModalContainer_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Modals/DialogueModalContainer.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/SelectRow.client.js
const SelectRow_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const SelectRow_client = ({ $$typeof: SelectRow_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/SettingsBar/SelectRow.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/SettingsBar/RefreshButton.client.js
const RefreshButton_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const RefreshButton_client = ({ $$typeof: RefreshButton_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/SettingsBar/RefreshButton.client.js", name: "default" });


// EXTERNAL MODULE: external "process"
var external_process_ = __webpack_require__("process");
;// CONCATENATED MODULE: ./config.js

const localConfig = {
    apiUrl: `${external_process_.env.KANGAS_PROTOCOL || "http"}://${external_process_.env.KANGAS_HOST}:${external_process_.env.KANGAS_BACKEND_PORT}/datagrid/`,
    defaultDecimalPrecision: 5,
    locale: "en-US",
    isColab: external_process_.env.IN_COLAB === "True"
};
/* harmony default export */ const config_0 = (localConfig);

;// CONCATENATED MODULE: ./components/SettingsBar/SettingsBar.server.js






const KangasButton = ()=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "button-outline",
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx("img", {
                src: "/favicon.png"
            }),
            /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "Kangas"
            })
        ]
    });
const StatusText = ({ status  })=>{
    const items = Object.keys(status.data).map((item)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("li", {
            className: "kangas-list-item",
            children: [
                /*#__PURE__*/ jsx_runtime_.jsx("span", {
                    className: "kangas-item",
                    children: item
                }),
                ": ",
                /*#__PURE__*/ jsx_runtime_.jsx("span", {
                    className: "kangas-value",
                    children: status.data[item]
                })
            ]
        }));
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx("h1", {
                className: "kangas-title",
                children: "\uD83E\uDD98 Kangas DataGrid"
            }),
            /*#__PURE__*/ jsx_runtime_.jsx("hr", {}),
            /*#__PURE__*/ jsx_runtime_.jsx("p", {
                className: "kangas-text",
                children: "\xa9 2022 Kangas DataGrid Development Team"
            }),
            /*#__PURE__*/ jsx_runtime_.jsx("div", {
                className: "kangas-text",
                children: items
            }),
            /*#__PURE__*/ (0,jsx_runtime_.jsxs)("p", {
                className: "kangas-text",
                children: [
                    "For help, contributions, examples, and discussions, see: ",
                    /*#__PURE__*/ jsx_runtime_.jsx("a", {
                        href: "https://www.github.com/comet-ml/kangas",
                        target: "_blank",
                        children: "github.com/comet-ml/kangas"
                    })
                ]
            }),
            /*#__PURE__*/ (0,jsx_runtime_.jsxs)("p", {
                className: "kangas-text",
                children: [
                    "Consider giving us a github ",
                    /*#__PURE__*/ jsx_runtime_.jsx("span", {
                        className: "kangas-item",
                        children: "\u272D"
                    }),
                    "!"
                ]
            })
        ]
    });
};
const SettingsBarServer = ({ query , matrices , columns , options , status , completions  })=>{
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        id: "settings-bar",
        children: [
            /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                id: "nav-bar-1",
                children: [
                    /*#__PURE__*/ jsx_runtime_.jsx(DialogueModalContainer_client, {
                        fullScreen: false,
                        toggleElement: /*#__PURE__*/ jsx_runtime_.jsx(KangasButton, {}),
                        children: /*#__PURE__*/ jsx_runtime_.jsx(StatusText, {
                            status: status
                        })
                    }),
                    /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                        id: "matrix-select",
                        className: "select-row",
                        children: [
                            /*#__PURE__*/ jsx_runtime_.jsx(MatrixSelect_client, {
                                query: query,
                                options: matrices
                            }),
                            /*#__PURE__*/ jsx_runtime_.jsx(RefreshButton_client, {
                                query: query
                            })
                        ]
                    })
                ]
            }),
            /*#__PURE__*/ jsx_runtime_.jsx("div", {
                id: "nav-bar",
                children: /*#__PURE__*/ jsx_runtime_.jsx(SelectRow_client, {
                    columns: columns,
                    query: query,
                    options: options,
                    completions: completions
                })
            })
        ]
    });
};
/* harmony default export */ const SettingsBar_server = (SettingsBarServer);

      const __next_rsc__ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/page.client.js
const page_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const page_client = ({ $$typeof: page_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/page.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/ExpandOverlay.client.js
const ExpandOverlay_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ExpandOverlay_client = ({ $$typeof: ExpandOverlay_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/ExpandOverlay.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/useData.js
const cache = {
    expiration: null
};
function clearCache() {
    for(const key in cache){
        delete cache[key];
    }
}
function useData(key, fetcher) {
    if (!cache[key]?.func || cache[key]?.created < cache.expiration) {
        let data;
        let error;
        let promise;
        const created = Date.now();
        cache[key] = {
            func: ()=>{
                if (error !== undefined || data !== undefined) return {
                    data,
                    error
                };
                if (!promise) {
                    promise = fetcher().then((r)=>data = r)// Convert all errors to plain string for serialization
                    .catch((e)=>error = e + "");
                }
                throw promise;
            },
            created
        };
    }
    return cache[key].func();
}
const updateExpiration = (time)=>{
    if (time) cache.expiration = time;
};


;// CONCATENATED MODULE: ./components/skeletons.js

function Skeletons() {
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        children: "Loading"
    });
};

;// CONCATENATED MODULE: external "node:buffer"
const external_node_buffer_namespaceObject = require("node:buffer");
;// CONCATENATED MODULE: ./lib/hashQuery.js

// Simple helper to generate a hash from a query object. We use this because
// our caching system, which is necessary to use React.Suspense, needs to assign a
// unique key to each distinct query.
const hashQuery = (query)=>{
    return external_node_buffer_namespaceObject.Buffer.from(JSON.stringify(query)).toString("base64");
};
/* harmony default export */ const lib_hashQuery = (hashQuery);

;// CONCATENATED MODULE: ./lib/fetchData.js
// Return type can be either json or blob, not case-sensitive
const fetchData_fetchData = async ({ url , query ={} , method ="POST" , returnType ="json" ,  })=>{
    const request = {
        method,
        headers: {
            "Content-Type": "application/json"
        }
    };
    // Attaching a body to a GET request will throw an error
    if (method === "POST") request["body"] = JSON.stringify(query);
    // For GET requests, we have to parse the query into a url
    let getUrl = null;
    if (method === "GET") {
        const params = new URLSearchParams(query);
        getUrl = `${url}?${params.toString()}`;
    }
    const res = await fetch(getUrl || url, request);
    if (res.status !== 200) {
        throw new Error(`Status ${res.status}`);
    }
    if (returnType.toLowerCase() === "json") return res.json();
    if (returnType.toLowerCase() === "blob") return res.blob();
    if (returnType.toLowerCase() === "text") return res.text();
    throw `${returnType} is not a valid return type. Please choose either JSON or Blob`;
};
/* harmony default export */ const lib_fetchData = (fetchData_fetchData);

;// CONCATENATED MODULE: ./lib/fetchTable.js
// Config

// Utils

const fetchTable = async (query)=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}query`,
        query
    });
    // Can eventually implement transformations
    return data;
};
/* harmony default export */ const lib_fetchTable = (fetchTable);

;// CONCATENATED MODULE: ./lib/fetchStatus.js
// Config

// Utils

const fetchStatus = async ()=>{
    const result = await lib_fetchData({
        url: `${config_0.apiUrl}status`,
        method: "GET"
    });
    return result;
};
/* harmony default export */ const lib_fetchStatus = (fetchStatus);

;// CONCATENATED MODULE: ./lib/fetchCompletions.js
// Config

// Utils

const fetchCompletions = async (dgid)=>{
    if (dgid) {
        const data = await lib_fetchData({
            url: `${config_0.apiUrl}completions`,
            query: {
                dgid
            },
            method: "POST"
        });
        return data;
    }
    return {};
};
/* harmony default export */ const lib_fetchCompletions = (fetchCompletions);

;// CONCATENATED MODULE: ./stubs.js
const STUB_QUERY_ARGS = {
    dgid: null,
    refresh: false,
    limit: 10
};
const STUB_MATRICES = (/* unused pure expression or super */ null && ([]));
const EMPTY_TABLE = {
    columns: [
        "row-id",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F"
    ],
    columnTypes: [
        "ROW_ID",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER",
        "PLACEHOLDER"
    ],
    nrows: 9,
    ncols: 8,
    total: 9,
    rows: [
        {
            "row-id": 1,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 2,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 3,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 4,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 5,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 6,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 7,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 8,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        },
        {
            "row-id": 9,
            A: " ",
            B: " ",
            C: " ",
            D: " ",
            E: " ",
            F: " "
        }
    ]
};

;// CONCATENATED MODULE: ./lib/fetchAsset.js
// Config

// Utils

const fetchAsset = async ({ assetId , dgid , returnUrl =false , returnType ="blob" , thumbnail =false ,  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}download`,
        query: {
            assetId,
            dgid,
            thumbnail
        },
        method: "GET",
        returnType
    });
    if (returnUrl) {
        const arrayBuffer = await data.arrayBuffer();
        const dataUrl = Buffer.from(arrayBuffer).toString("base64");
        return dataUrl;
    }
    return data;
};
/* harmony default export */ const lib_fetchAsset = (fetchAsset);

;// CONCATENATED MODULE: ./node_modules/next/image.js
const image_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const next_image = ({ $$typeof: image_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/node_modules/next/image.js", name: "" });


;// CONCATENATED MODULE: ./components/Cells/Image/ImageCell.server.js


// Config
// Utils



const ImageCell = ({ value , dgid  })=>{
    const { assetId  } = value;
    // Fetch this here, so it is available in the expanded view:
    /* eslint-disable no-unused-vars */ const image = useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnUrl: true
        }));
    /* eslint-enable no-unused-vars */ const thumbnail = useData(`${assetId}-thumbnail`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnUrl: true,
            thumbnail: true
        }));
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content image",
        children: /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
            fallback: /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "fallback"
            }),
            children: /*#__PURE__*/ jsx_runtime_.jsx(next_image, {
                src: `data:application/octet-stream;base64,${thumbnail.data}`,
                layout: "fill",
                objectFit: "contain",
                alt: "DataGrid Image Thumbnail"
            })
        })
    });
};
/* harmony default export */ const ImageCell_server = (ImageCell);

      const ImageCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./lib/fetchAssetGroupThumbnail.js
// Config

// Utils

const fetchAssetGroupThumbnail = async ({ query  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-group-thumbnail`,
        query,
        method: "POST",
        returnType: "blob"
    });
    const arrayBuffer = await data.arrayBuffer();
    const dataUrl = Buffer.from(arrayBuffer).toString("base64");
    return dataUrl;
};
/* harmony default export */ const lib_fetchAssetGroupThumbnail = (fetchAssetGroupThumbnail);

;// CONCATENATED MODULE: ./lib/fetchAssetGroup.js
// Config

// Utils


const fetchAssetGroup = async ({ query , returnUrl =false , returnType ="json" , size =0 , thumbnail =false ,  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-group`,
        query,
        method: "POST",
        returnType
    });
    if (returnUrl && data?.values?.length) {
        const { dgid  } = query;
        const end = size ? size : data.values.length;
        const assetPromises = Promise.all(data.values.slice(0, end).map((assetId)=>{
            return lib_fetchAsset({
                assetId,
                dgid,
                returnUrl: true,
                thumbnail
            });
        })).then((dataUrls)=>dataUrls);
        return assetPromises;
    }
    return data;
};
/* harmony default export */ const lib_fetchAssetGroup = (fetchAssetGroup);

;// CONCATENATED MODULE: ./components/Cells/Image/Group.server.js


// Server Components

// Utils




const ImageGroupCell = ({ value  })=>{
    const query = {
        ...value,
        gallerySize: [
            3,
            2
        ],
        backgroundColor: [
            255,
            255,
            255
        ],
        imageSize: [
            100,
            55
        ],
        borderWidth: 2
    };
    // gallerySize is the number of columns, rows of the gallery image
    // imageSize is the max-width, max-height in pixels of each thumbnail image
    // in the gallery
    const countQuery = {
        ...value,
        columnLimit: 0
    };
    const groupThumbnail = useData(`${lib_hashQuery(query)}`, ()=>lib_fetchAssetGroupThumbnail({
            query
        }));
    const groupDetails = useData(`${lib_hashQuery(countQuery)}`, ()=>lib_fetchAssetGroup({
            query: countQuery
        }));
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content image-group",
        children: /*#__PURE__*/ (0,jsx_runtime_.jsxs)(external_react_.Suspense, {
            fallback: /*#__PURE__*/ jsx_runtime_.jsx("span", {
                children: "fallback"
            }),
            children: [
                /*#__PURE__*/ jsx_runtime_.jsx("span", {
                    children: `${groupDetails.data.total} Images`
                }),
                /*#__PURE__*/ jsx_runtime_.jsx(next_image, {
                    src: `data:application/octet-stream;base64,${groupThumbnail.data}`,
                    layout: "fill",
                    objectFit: "contain",
                    alt: "Image Group Thumbnail"
                })
            ]
        })
    });
};
/* harmony default export */ const Group_server = (ImageGroupCell);

      const Group_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./lib/fetchAssetMetadata.js
// Config

// Utils

const fetchAssetMetadata_fetchAsset = async ({ assetId , dgid  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-metadata`,
        query: {
            assetId,
            dgid
        },
        method: "POST",
        returnType: "json"
    });
    return data;
};
/* harmony default export */ const fetchAssetMetadata = (fetchAssetMetadata_fetchAsset);

;// CONCATENATED MODULE: ./components/Cells/Image/ImageCanvas.client.js
const ImageCanvas_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ImageCanvas_client = ({ $$typeof: ImageCanvas_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/Image/ImageCanvas.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Image/Expanded.server.js





// Config

// Client

const ExpandedImageCell = ({ value , dgid  })=>{
    const { assetId  } = value;
    const url = `${config_0.apiUrl}download?assetId=${assetId}&dgid=${dgid}`;
    const metadata = useData(`${lib_hashQuery({
        assetId,
        dgid
    })}`, ()=>fetchAssetMetadata({
            assetId,
            dgid
        })).data;
    return /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
        fallback: /*#__PURE__*/ jsx_runtime_.jsx(jsx_runtime_.Fragment, {
            children: "Loading"
        }),
        children: /*#__PURE__*/ jsx_runtime_.jsx(ImageCanvas_client, {
            url: url,
            dgid: dgid,
            assetId: assetId,
            inheritedMetadata: metadata
        })
    });
};
/* harmony default export */ const Expanded_server = (ExpandedImageCell);

      const Expanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./lib/fetchAssetGroupMetadata.js
// Config

// Utils

const fetchAssetGroupMetadata = async ({ query , returnType ="json"  })=>{
    const data = await lib_fetchData({
        url: `${config_0.apiUrl}asset-group-metadata`,
        query,
        method: "POST",
        returnType
    });
    return data;
};
/* harmony default export */ const lib_fetchAssetGroupMetadata = (fetchAssetGroupMetadata);

;// CONCATENATED MODULE: ./components/Cells/Image/ExpandedGroup.server.js


// Server Components
// Client Components
// Config

// Util





const ExpandedGroupImageCell = ({ value , dgid  })=>{
    const metadataQuery = {
        ...value,
        metadataPath: "labels"
    };
    const images = useData(`${lib_hashQuery(value)}`, ()=>lib_fetchAssetGroup({
            query: value,
            thumbnail: true
        })).data;
    const labels = useData(`${lib_hashQuery(metadataQuery)}`, ()=>lib_fetchAssetGroupMetadata({
            query: metadataQuery
        })).data;
    const metadata = JSON.stringify({
        labels
    });
    const urls = images.values.map((id)=>`${config_0.apiUrl}download?assetId=${id}&dgid=${dgid}`);
    return /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
        fallback: /*#__PURE__*/ jsx_runtime_.jsx("div", {
            children: "loading"
        }),
        children: /*#__PURE__*/ jsx_runtime_.jsx(ImageCanvas_client, {
            urls: urls,
            inheritedMetadata: metadata,
            dgid: dgid
        })
    });
};
/* harmony default export */ const ExpandedGroup_server = (ExpandedGroupImageCell);

      const ExpandedGroup_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./lib/truncateValue.js
// Config

const countDecimals = (value)=>{
    if (Math.floor(value) === value) return 0;
    const [, decimalPart = ""] = value.toString().split(".");
    return decimalPart.length;
};
const truncateValue = (value, customDecimalsPrecision)=>{
    const decimalsPrecision = customDecimalsPrecision ?? config_0.defaultDecimalPrecision;
    if (decimalsPrecision === null) return value;
    const numberValue = Number(value);
    if (isNaN(numberValue)) return value;
    if (Number.isInteger(numberValue) || countDecimals(numberValue) <= decimalsPrecision) {
        return numberValue;
    }
    const exponential = 10 ** decimalsPrecision;
    return Math.floor(numberValue * exponential) / exponential;
};
/* harmony default export */ const lib_truncateValue = (truncateValue);

;// CONCATENATED MODULE: ./lib/formatValue.js

function formatValue(value, columnType) {
    if (value === null) {
        return "None";
    }
    let retval = value;
    if (columnType === "DATETIME") {
        const timestampObj = new UnixTime(value);
        retval = timestampObj.format("YYYY-MM-DD HH:mm:ss");
    } else if (columnType === "FLOAT") {
        retval = lib_truncateValue(value).toString();
    } else if (typeof value !== "string") {
        retval = value.toString();
    }
    return retval;
}
function pad(item, size, padding = "0") {
    return String(item).padStart(size, padding);
}
class UnixTime {
    constructor(datetime){
        this.obj = new Date(datetime * 1000);
        this.year = pad(this.obj.getFullYear(), 4);
        this.month = pad(this.obj.getMonth() + 1, 2);
        this.day = pad(this.obj.getDate(), 2);
        this.hour = pad(this.obj.getHours(), 2);
        this.minute = pad(this.obj.getMinutes(), 2);
        this.second = pad(this.obj.getSeconds(), 2);
    }
    format() {
        // Hard coded for now: 'YYYY-MM-DD HH:mm:ss'
        if (this.hour === "00" && this.minute === "00" && this.second === "00") {
            return `${this.year}-${this.month}-${this.day}`;
        } else {
            return `${this.year}-${this.month}-${this.day} ${this.hour}:${this.minute}:${this.second}`;
        }
    }
}
/* harmony default export */ const lib_formatValue = (formatValue);

;// CONCATENATED MODULE: ./components/Cells/DateCell.server.js


const DateCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "DATETIME")}`
    });
};
/* harmony default export */ const DateCell_server = (DateCell);

      const DateCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/TextCell.server.js


const TextCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "TEXT")}`
    });
};
/* harmony default export */ const TextCell_server = (TextCell);

      const TextCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/FloatCell.server.js

// Utils

const FloatCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${lib_formatValue(value, "FLOAT")}`
    });
};
/* harmony default export */ const FloatCell_server = (FloatCell);

      const FloatCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/FloatExpanded.server.js

// Config

const FloatExpanded = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content",
        children: `${value}`
    });
};
/* harmony default export */ const FloatExpanded_server = (FloatExpanded);

      const FloatExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/AudioCell.server.js

// Config

// Client components
//import Player from '../Player/Player.client';
// Util


// To get our fun waveform effect, we need to implement something better than wavesurfer.js. For now, the native
// audio element works fantastic. Users can control playback, skip around, etc.
const AudioCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const image = useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid
        }));
    // Wavesurfer is going to be difficult with SSR. Need to reconfigure.
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content audio",
        children: /*#__PURE__*/ jsx_runtime_.jsx("audio", {
            src: "",
            controls: true
        })
    });
/*
    return (
        <Player
        src={`${cell.src}`}
        style={{ width: '100%' }}
        height={90}
        />
    )*/ };
/* harmony default export */ const AudioCell_server = (AudioCell);

      const AudioCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/VideoCell.server.js

// Config

// Util


/* In comet-react, we use react-player, which gives us out of the box support for YouTube/Vimeo/Wistia links etc.
However, it is also heavy and completely client side. The question is: How big is that use case? How often are users
logging links to 3rd party video platforms as part of their data vs. logging actual video files? */ const VideoCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    //const video = useData(`${assetId}`, () => fetchAsset({ assetId, dgid, returnUrl: true}));
    const video_url = `${config_0.apiUrl}download?assetId=${assetId}&dgid=${dgid}`;
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content video",
        children: /*#__PURE__*/ jsx_runtime_.jsx("video", {
            src: video_url,
            controls: true
        })
    });
};
/* harmony default export */ const VideoCell_server = (VideoCell);

      const VideoCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/TextAssetCell.server.js



const TextAssetCell = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const image = useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid
        }));
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content text-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx("pre", {
            children: /*#__PURE__*/ jsx_runtime_.jsx("code", {
                children: "text"
            })
        })
    });
};
/* harmony default export */ const TextAssetCell_server = (TextAssetCell);

      const TextAssetCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/CurveAssetCell.client.js
const CurveAssetCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CurveAssetCell_client = ({ $$typeof: CurveAssetCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/CurveAssetCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/generateChartColor.js
// Color functions
/*
// Full color spectrum:
const getUniqueColor = (hash) => {
    const n = hash % 124;
    // Must return lowercase hex
    // so that getContrastingColor will work
    const rgb = [0, 0, 0];
    let counter = n;
    for (let i = 0; i < 24; i++) {
	rgb[i % 3] <<= 1;
	rgb[i % 3] |= counter & 0x01;
	counter >>= 1;
    }
    return `#${rgb.reduce(
      (a, c) => (c > 0x0f ? c.toString(16) : `0${c.toString(16)}`) + a,
      ''
    )}`;
};
*/ // Constrained to a given color pallete:
const getUniqueColor = (hash)=>{
    // 144 color palette
    /* 
    const colors = [
	'#1a293f', '#22334d', '#2a3c5a', '#324669', '#3a5077', '#435a86', '#4d6595', '#5670a4', '#607ab4', '#6b85c4', '#7690d4', '#819be4',
	'#2a253e', '#342e4a', '#3e3757', '#483f64', '#534972', '#5e5280', '#695b8e', '#75659c', '#806fab', '#8d79ba', '#9983c9', '#a68dd8',
	'#3a223a', '#452a46', '#513252', '#5e3a5f', '#6a426b', '#774b78', '#845486', '#925c93', '#9f65a1', '#ad6faf', '#bb78bd', '#c981cb',
	'#451c2e', '#522238', '#602941', '#6d2f4b', '#7b3655', '#8a3d60', '#98456a', '#a74c75', '#b65380', '#c65b8b', '#d56396', '#e56ba1',
	'#4a1a1e', '#571f24', '#65252b', '#732b31', '#813138', '#8f383f', '#9d3e47', '#ac454e', '#bb4b55', '#cb525d', '#da5964', '#ea606c',
	'#0c343c', '#11414b', '#154e5a', '#1a5c69', '#1f6a79', '#247988', '#298799', '#2e96a9', '#33a6ba', '#38b5cb', '#3dc5dd', '#42d5ee',
	'#0a382a', '#0f4636', '#135542', '#18644f', '#1c745c', '#21846a', '#259578', '#2aa686', '#2fb795', '#33c9a4', '#38dab3', '#3cecc3',
	'#222f11', '#2d3d18', '#394c1f', '#445b27', '#516a2f', '#5d7b37', '#6a8b3f', '#779c48', '#84ad51', '#91bf5a', '#9fd163', '#ace36c',
	'#4f4114', '#5b4b18', '#66551c', '#725f20', '#7e6925', '#8a7429', '#967e2d', '#a28932', '#af9437', '#bc9f3b', '#c8ab40', '#d5b645',
	'#492c12', '#563517', '#643d1c', '#714621', '#7f5026', '#8d592b', '#9c6231', '#ab6c36', '#ba763c', '#c98041', '#d88a47', '#e8944d',
	'#462514', '#542d1a', '#623520', '#713e26', '#80472c', '#8f5032', '#9f5939', '#af6240', '#bf6c46', '#cf754d', '#e07f54', '#f1895b',
	'#daf96b', '#a4f986', '#6df6a9', '#35efcb', '#1de5e7', '#53d7f8', '#8ac6fc', '#b8b2f1', '#db9ed9', '#f08bb9', '#f77f95', '#f07b72'
    ];
    */ // 15 color palette
    const colors = [
        "#ffd51d",
        "#ffbd00",
        "#ff8900",
        "#fb7628",
        "#ff4747",
        "#e51772",
        "#cf0057",
        "#6e1d89",
        "#860dab",
        "#49a5bd",
        "#0096c7",
        "#00b4d8",
        "#12a592",
        "#16cab2",
        "#41ead4", 
    ];
    return colors[hash % colors.length];
};
const getColor = (text = "0")=>{
    // Must return lowercase hex
    // so that getContrastingColor will work
    if ([
        "1",
        "true",
        "t",
        "yes"
    ].includes(text.toLowerCase())) return "#12a592"; // green from palette
    if ([
        "0",
        "false",
        "f",
        "no"
    ].includes(text.toLowerCase())) return "#cf0057"; // red from palette
    const hash = [
        ...text
    ].reduce((acc, char)=>{
        return char.charCodeAt(0) + ((acc << 5) - acc);
    }, 0);
    return getUniqueColor(Math.abs(hash));
};
const hexToRgb = (hex)=>{
    const result = hex.match(/^#([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/);
    return [
        parseInt(result[1], 16),
        parseInt(result[2], 16),
        parseInt(result[3], 16), 
    ];
};
const getContrastingColor = (hex)=>{
    const colors = hexToRgb(hex);
    const r = colors[0];
    const g = colors[1];
    const b = colors[2];
    const o = Math.round((r * 299 + g * 587 + b * 114) / 1000);
    return o > 125 ? "black" : "white";
};

;// CONCATENATED MODULE: ./components/Cells/CurveAssetCell.server.js

// Client components

// Util



// TODO Create a helper called generateLayout that also generates data.
const CurveAssetCellServer = ({ value , dgid  })=>{
    const { type , assetId , assetType  } = value;
    const asset = useData(`${assetId}`, ()=>lib_fetchAsset({
            assetId,
            dgid,
            returnType: "json"
        }));
    const { data , error  } = asset;
    const chartData = [
        {
            type: "line",
            x: data.x,
            y: data.y,
            marker: {
                color: getColor(data.name)
            }
        }, 
    ];
    const layout = {
        paper_bgcolor: "white",
        plot_bgcolor: "white",
        width: 120,
        height: 120,
        margin: {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 0
        },
        showlegend: false,
        xaxis: {
            visible: false,
            showticklabels: false
        },
        yaxis: {
            visible: false,
            showticklabels: false
        }
    };
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content curve-asset",
        children: /*#__PURE__*/ jsx_runtime_.jsx(CurveAssetCell_client, {
            chartData: chartData,
            layout: layout
        })
    });
};
/* harmony default export */ const CurveAssetCell_server = (CurveAssetCellServer);

      const CurveAssetCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/BooleanCell.client.js
const BooleanCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const BooleanCell_client = ({ $$typeof: BooleanCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/BooleanCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/BooleanCell.server.js

// Client components

const BooleanCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content boolean",
        children: /*#__PURE__*/ jsx_runtime_.jsx(BooleanCell_client, {
            value: value
        })
    });
};
/* harmony default export */ const BooleanCell_server = (BooleanCell);

      const BooleanCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/JSONCell.server.js

const JSONCell = ({ value  })=>{
    const jsonValue = value ? JSON.stringify(value) : "None";
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content json",
        children: jsonValue
    });
};
/* harmony default export */ const JSONCell_server = (JSONCell);

      const JSONCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/VectorCell.server.js

const VectorCell = ({ value  })=>{
    const stringValue = value ? value : "None";
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content json",
        children: stringValue
    });
};
/* harmony default export */ const VectorCell_server = (VectorCell);

      const VectorCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/PlaceholderCell.server.js

const PlaceholderCell = ({ value  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "placeholder-cell"
    });
};
/* harmony default export */ const PlaceholderCell_server = (PlaceholderCell);

      const PlaceholderCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupCell.client.js
const HistogramGroupCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const HistogramGroupCell_client = ({ $$typeof: HistogramGroupCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/Histogram/HistogramGroupCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/DeferredCell.client.js
const DeferredCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const DeferredCell_client = ({ $$typeof: DeferredCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/DeferredCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupCell.server.js

// Client components

// Util

// TODO Create a helper called generateLayout that also generates data.
const HistogramGroupCell = ({ value , dgid , defer  })=>{
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "cell-content histogram",
        children: [
            !defer && /*#__PURE__*/ jsx_runtime_.jsx(HistogramGroupCell_client, {
                value: value
            }),
            defer && /*#__PURE__*/ jsx_runtime_.jsx(DeferredCell_client, {
                children: /*#__PURE__*/ jsx_runtime_.jsx(HistogramGroupCell_client, {
                    value: value
                })
            })
        ]
    });
};
/* harmony default export */ const HistogramGroupCell_server = (HistogramGroupCell);

      const HistogramGroupCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupExpanded.client.js
const HistogramGroupExpanded_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const HistogramGroupExpanded_client = ({ $$typeof: HistogramGroupExpanded_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/Histogram/HistogramGroupExpanded.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Histogram/HistogramGroupExpanded.server.js


const HistogramGroupExpanded = ({ value , dgid  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content histogram",
        children: /*#__PURE__*/ jsx_runtime_.jsx(HistogramGroupExpanded_client, {
            value: value
        })
    });
};
/* harmony default export */ const HistogramGroupExpanded_server = (HistogramGroupExpanded);

      const HistogramGroupExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupCell.client.js
const CategoryGroupCell_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CategoryGroupCell_client = ({ $$typeof: CategoryGroupCell_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/Category/CategoryGroupCell.client.js", name: "default" });


;// CONCATENATED MODULE: ./lib/fetchCategory.js
// Config

// Utils

const fetchCategory = async ({ query  })=>{
    const data = await fetchData({
        url: `${config.apiUrl}category`,
        query,
        method: "POST"
    });
    return data;
};
/* harmony default export */ const lib_fetchCategory = ((/* unused pure expression or super */ null && (fetchCategory)));

;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupCell.server.js


// Client components


// Util





// TODO Create a helper called generateLayout that also generates data.
const CategoryGroupCell = ({ value , dgid , defer  })=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
        className: "cell-content category-chart",
        children: [
            !defer && /*#__PURE__*/ jsx_runtime_.jsx(CategoryGroupCell_client, {
                value: value
            }),
            defer && /*#__PURE__*/ jsx_runtime_.jsx(DeferredCell_client, {
                children: /*#__PURE__*/ jsx_runtime_.jsx(CategoryGroupCell_client, {
                    value: value
                })
            })
        ]
    });
/* harmony default export */ const CategoryGroupCell_server = (CategoryGroupCell);

      const CategoryGroupCell_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupExpanded.client.js
const CategoryGroupExpanded_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const CategoryGroupExpanded_client = ({ $$typeof: CategoryGroupExpanded_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/Category/CategoryGroupExpanded.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/Category/CategoryGroupExpanded.server.js


// Client components

// Util





// TODO Create a helper called generateLayout that also generates data.
const CategoryGroupExpanded_server_CategoryGroupCell = ({ value , dgid  })=>{
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "cell-content category-chart",
        children: /*#__PURE__*/ jsx_runtime_.jsx(CategoryGroupExpanded_client, {
            value: value
        })
    });
};
/* harmony default export */ const CategoryGroupExpanded_server = (CategoryGroupExpanded_server_CategoryGroupCell);

      const CategoryGroupExpanded_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./lib/makeComponentMap.js




















const SINGLE_VALUE_WIDTH = 75;
const GROUPED_ASSET_WIDTH = 150;
const columnTypeMap = {
    BOOLEAN: {
        component: BooleanCell_server,
        expandedComponent: BooleanCell_server,
        groupComponent: CategoryGroupCell_server,
        expandedGroupComponent: CategoryGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    TEXT: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: CategoryGroupCell_server,
        expandedGroupComponent: CategoryGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    INTEGER: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: CategoryGroupCell_server,
        expandedGroupComponent: CategoryGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    FLOAT: {
        component: FloatCell_server,
        expandedComponent: FloatExpanded_server,
        groupComponent: HistogramGroupCell_server,
        expandedGroupComponent: HistogramGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    DATETIME: {
        component: DateCell_server,
        expandedComponent: DateCell_server,
        groupComponent: HistogramGroupCell_server,
        expandedGroupComponent: HistogramGroupExpanded_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH
    },
    JSON: {
        component: JSONCell_server,
        expandedComponent: JSONCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: 300,
        groupedWidth: 300
    },
    ROW_ID: {
        component: TextCell_server,
        expandedComponent: TextCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: SINGLE_VALUE_WIDTH
    },
    "IMAGE-ASSET": {
        component: ImageCell_server,
        expandedComponent: Expanded_server,
        groupComponent: Group_server,
        expandedGroupComponent: ExpandedGroup_server,
        singleWidth: SINGLE_VALUE_WIDTH * 2,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "AUDIO-ASSET": {
        component: AudioCell_server,
        expandedComponent: AudioCell_server,
        groupComponent: AudioCell_server,
        expandedGroupComponent: AudioCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "CURVE-ASSET": {
        component: CurveAssetCell_server,
        expandedComponent: CurveAssetCell_server,
        groupComponent: CurveAssetCell_server,
        expandedGroupComponent: CurveAssetCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "TEXT-ASSET": {
        component: TextAssetCell_server,
        expandedComponent: TextAssetCell_server,
        groupComponent: TextAssetCell_server,
        expandedGroupComponent: TextAssetCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    "VIDEO-ASSET": {
        component: VideoCell_server,
        expandedComponent: VideoCell_server,
        groupComponent: VideoCell_server,
        expandedGroupComponent: VideoCell_server,
        singleWidth: SINGLE_VALUE_WIDTH,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: true
    },
    PLACEHOLDER: {
        component: PlaceholderCell_server,
        expandedComponent: PlaceholderCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: SINGLE_VALUE_WIDTH * 2,
        groupedWidth: GROUPED_ASSET_WIDTH,
        isAsset: false
    },
    VECTOR: {
        component: VectorCell_server,
        expandedComponent: VectorCell_server,
        groupComponent: PlaceholderCell_server,
        expandedGroupComponent: PlaceholderCell_server,
        singleWidth: 300,
        groupedWidth: 300
    }
};
const makeComponentMap = (table)=>{
    const { columnTypes , columns , ncols  } = table;
    // Make sure our columns aren't foo-bar'd
    if (!columns || columns.length !== ncols) return null;
    const nameToComponent = {};
    columns.forEach((name, idx)=>{
        const type = columnTypes[idx];
        nameToComponent[name] = {
            component: columnTypeMap[type].component,
            type,
            accessor: name,
            idx,
            singleWidth: columnTypeMap[type].singleWidth,
            groupedWidth: columnTypeMap[type].groupedWidth,
            isAsset: columnTypeMap[type].isAsset
        };
    });
    return nameToComponent;
};
/* harmony default export */ const lib_makeComponentMap = ((/* unused pure expression or super */ null && (makeComponentMap)));

;// CONCATENATED MODULE: ./components/SettingsBar/Paging.client.js
const Paging_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const Paging_client = ({ $$typeof: Paging_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/SettingsBar/Paging.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/FooterRow.server.js


const FooterRow = ({ query , total  })=>{
    const pages = Math.ceil(total / (query?.limit || total));
    const pagination = Array.from({
        length: pages
    }, (val, idx)=>idx + 1);
    return /*#__PURE__*/ jsx_runtime_.jsx("div", {
        className: "footer-row",
        children: /*#__PURE__*/ jsx_runtime_.jsx(Paging_client, {
            query: query,
            total: total,
            pagination: pagination
        })
    });
};
/* harmony default export */ const FooterRow_server = (FooterRow);

      const FooterRow_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    
;// CONCATENATED MODULE: ./components/SettingsBar/Imports.client.js
const Imports_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const Imports_client = ({ $$typeof: Imports_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/SettingsBar/Imports.client.js", name: "default" });


;// CONCATENATED MODULE: ./components/Cells/ClientContext.client.js
const ClientContext_client_MODULE_REFERENCE = Symbol.for('react.module.reference');
/* harmony default export */ const ClientContext_client = ({ $$typeof: ClientContext_client_MODULE_REFERENCE, filepath: "/home/dblank/comet/kangas/frontend/components/Cells/ClientContext.client.js", name: "default" });


// EXTERNAL MODULE: external "@mui/material"
var material_ = __webpack_require__("@mui/material");
;// CONCATENATED MODULE: ./pages/index.server.js

/* eslint-disable react/jsx-key */ // React

// Server Components

// Client Components


// Utils












// If not imported here, the import in page.client.js will fail

const Root = ({ query , matrices , expiration  })=>{
    /* eslint-disable no-unused-vars */ updateExpiration(expiration);
    const { data: table , tableError  } = useData(`query-${lib_hashQuery({
        query
    })}`, ()=>lib_fetchTable(query));
    const status = useData(`status`, ()=>lib_fetchStatus());
    const { data: allColumns , colError  } = useData(`query-${lib_hashQuery({
        query: {
            ...query,
            select: "*",
            limit: 1
        }
    })}`, ()=>lib_fetchTable(query));
    /* eslint-enable no-unused-vars */ const { dgid  } = query;
    const { columnTypes , columns , rows , total  } = table ?? EMPTY_TABLE;
    const { data: completions  } = useData(`completions-${dgid}`, ()=>lib_fetchCompletions(dgid));
    const columnOptions = allColumns ? allColumns?.columns?.filter((col)=>!col.endsWith("--metadata")) : [];
    // TODO Clean this up with .filter()
    const filteredColumns = [];
    const filteredColumnTypes = [];
    columns.forEach((columnName, idx)=>{
        if (!columnName.endsWith("--metadata")) {
            filteredColumnTypes.push(columnTypes[idx]);
            filteredColumns.push(columnName);
        }
    });
    // TODO Clean up
    const rowClass = !!query?.groupBy && query?.groupBy ? "row-group" : "row";
    const colClass = !!query?.groupBy && query?.groupBy ? "column-group cell-group" : "column cell";
    const headerClass = colClass.includes("group") ? "column-group" : "column";
    return /*#__PURE__*/ (0,jsx_runtime_.jsxs)(page_client, {
        children: [
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(Imports_client, {})
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(SettingsBar_server, {
                    query: query,
                    matrices: matrices,
                    columns: filteredColumns,
                    options: columnOptions,
                    status: status,
                    completions: completions
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(ClientContext_client, {
                    apiUrl: config_0.apiUrl,
                    otherUrl: config_0.apiUrl,
                    isColab: config_0.isColab,
                    children: /*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                        className: "table-root",
                        children: [
                            /*#__PURE__*/ jsx_runtime_.jsx("div", {
                                id: "header-row",
                                className: `${rowClass}`,
                                children: filteredColumns.map((col)=>/*#__PURE__*/ jsx_runtime_.jsx("div", {
                                        className: headerClass,
                                        title: col,
                                        children: col
                                    }))
                            }),
                            rows.map((row, ridx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                    className: `${rowClass}`,
                                    children: [
                                        filteredColumns.slice(0, 5).map((col, idx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                                className: `${colClass}`,
                                                children: [
                                                    !!query?.groupBy && query?.groupBy !== col ? columnTypeMap[filteredColumnTypes[idx]].groupComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    }) : columnTypeMap[filteredColumnTypes[idx]].component({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    }),
                                                    /*#__PURE__*/ jsx_runtime_.jsx(ExpandOverlay_client, {
                                                        children: !!query?.groupBy && query?.groupBy !== col ? columnTypeMap[filteredColumnTypes[idx]].expandedGroupComponent({
                                                            value: row[col],
                                                            dgid,
                                                            row,
                                                            col,
                                                            query
                                                        }) : columnTypeMap[filteredColumnTypes[idx]].expandedComponent({
                                                            value: row[col],
                                                            dgid,
                                                            row,
                                                            col
                                                        })
                                                    })
                                                ]
                                            }, `${ridx}-${idx}`)),
                                        filteredColumns.length > 5 && filteredColumns.slice(5).map((col, idx)=>/*#__PURE__*/ (0,jsx_runtime_.jsxs)("div", {
                                                className: `${colClass}`,
                                                children: [
                                                    !!query?.groupBy && query?.groupBy !== col ? columnTypeMap[filteredColumnTypes[idx + 5]].groupComponent({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col,
                                                        defer: true
                                                    }) : columnTypeMap[filteredColumnTypes[idx + 5]].component({
                                                        value: row[col],
                                                        dgid,
                                                        row,
                                                        col
                                                    }),
                                                    /*#__PURE__*/ jsx_runtime_.jsx(ExpandOverlay_client, {
                                                        children: !!query?.groupBy && query?.groupBy !== col ? columnTypeMap[filteredColumnTypes[idx + 5]].expandedGroupComponent({
                                                            value: row[col],
                                                            dgid,
                                                            row,
                                                            col,
                                                            query,
                                                            defer: true
                                                        }) : columnTypeMap[filteredColumnTypes[idx + 5]].expandedComponent({
                                                            value: row[col],
                                                            dgid,
                                                            row,
                                                            col
                                                        })
                                                    })
                                                ]
                                            }, `${ridx}-${idx + 5}`))
                                    ]
                                }, `row-${ridx}`))
                        ]
                    })
                })
            }),
            /*#__PURE__*/ jsx_runtime_.jsx(external_react_.Suspense, {
                fallback: /*#__PURE__*/ jsx_runtime_.jsx(Skeletons, {}),
                children: /*#__PURE__*/ jsx_runtime_.jsx(FooterRow_server, {
                    query: query,
                    total: total
                })
            })
        ]
    });
};
// The Next.js server knows to look for this function and apply it to the index.server page
const getServerSideProps = async (context)=>{
    const data = await fetch(`${config_0.apiUrl}list`);
    const matrices = await data.json();
    const props = {
        props: {
            matrices: matrices || [],
            query: {
                dgid: context.query?.datagrid || null,
                whereExpr: context.query?.filter || null,
                limit: 10
            },
            expiration: null
        }
    };
    return props;
};
/* harmony default export */ const index_server = (Root);

      const index_server_next_rsc_ = {
        __webpack_require__,
        server: true
      }
    

/***/ })

};
;

// load runtime
var __webpack_require__ = require("../webpack-runtime.js");
__webpack_require__.C(exports);
var __webpack_exec__ = (moduleId) => (__webpack_require__(__webpack_require__.s = moduleId))
var __webpack_exports__ = (__webpack_exec__("(sc_server)/./pages/index.server.js"));
module.exports = __webpack_exports__;

})();