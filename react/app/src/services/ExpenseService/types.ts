export type Expense = {
    id: number;
    title: string;
    cost: number;
    quantity: number;
    date: string; 
  }
  
  export type ExpenseCreate = {
    title: string;
    cost: number;
    quantity: number;
    date: string;
  }

  export type ExpenseUpdate = {
    title?: string;
    cost?: number;
    quantity?: number;
    date?: string;
  }

  export type PaginatedResponse = {
    results: Expense[];
    count: number;
    total_pages: number;
    next: boolean;
    previous: boolean;
    current_page: number;
    page_size: number;
  }
