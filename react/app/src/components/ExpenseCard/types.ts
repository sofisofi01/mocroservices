export type ExpenseCardProps = {
    id: number;
    title: string;
    cost: number;
    quantity: number;
    date: string;
    onChange?: (id:number) => void;
    onDelete?: (id:number) => void;
}