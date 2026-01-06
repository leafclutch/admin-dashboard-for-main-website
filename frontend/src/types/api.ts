
export interface ApiError {
  detail: string | Array<{ 
    msg: string; 
    loc: (string | number)[]; 
    type: string 
  }>;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
}