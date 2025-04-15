import { $http } from '.'

export const generateOutlineAPI = (params: { language: string; title: string; LLM: string }) => {
  return $http({
    method: 'GET',
    url: '/generate_outline',
    params,
  })
}

export const getKeywordAPI = (params: { content: string }) => {
  return $http({
    method: 'GET',
    url: '/get_keyword',
    params,
  })
}

export const searchPubmedAPI = (params: { keywords: string }) => {
  return $http({
    method: 'GET',
    url: '/search_pubmed',
    params,
  })
}

export const editAPI = (params: {
  language: string
  title: string
  prompt_outline: string
  paper: string
  LLM: string
}) => {
  return $http({
    method: 'GET',
    url: '/edit',
    data: params,
  })
}
