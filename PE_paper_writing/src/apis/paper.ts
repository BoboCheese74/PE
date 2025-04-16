import { $http } from '.'

export const generateOutlineAPI = (params: { language: string; title: string; LLM: string }) => {
  return $http({
    method: 'GET',
    url: '/generate_outline',
    params,
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` || '' },
  })
}

export const getKeywordAPI = (params: { content: string }) => {
  return $http({
    method: 'GET',
    url: '/get_keyword',
    params,
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` || '' },
  })
}

export const searchPubmedAPI = (params: { keywords: string }) => {
  return $http({
    method: 'GET',
    url: '/search_pubmed',
    params,
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` || '' },
  })
}

export const editAPI = (params: {
  language: string
  title: string
  LLM?: string
  prompt_outline: string
  paper: string
}) => {
  return $http({
    method: 'GET',
    url: '/edit',
    params,
    headers: { Authorization: `Bearer ${localStorage.getItem('token')}` || '' },
  })
}
