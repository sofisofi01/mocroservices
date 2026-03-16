import type { ExpenseCardProps } from "./types";
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Box,
  Chip,
  Button,
} from '@mui/material';
import { Edit, Delete } from '@mui/icons-material';

export function ExpenseCard({quantity, cost, title, id, date, onChange, onDelete}: ExpenseCardProps) {
    const formatDate = (dateString: string) => {
        return new Date(dateString).toLocaleDateString('ru-RU', {
          day: 'numeric',
          month: 'long',
          year: 'numeric'
        });
      };
    
      const totalCost = cost * quantity;
    
      const handleEdit = () => {
        if (onChange) {
          onChange(id);
        }
      };
    
      const handleDelete = () => {
        if (onDelete) {
          onDelete(id);
        }
      };

      return (
        <Card 
          sx={{ 
            height: '100%',
            display: 'flex',
            flexDirection: 'column',
          }}
        >
          <CardContent sx={{ flexGrow: 1 }}>
            <Box display="flex" justifyContent="space-between" alignItems="flex-start" mb={2}>
              <Typography variant="h6" component="p" fontWeight="bold" noWrap>
                {title}
              </Typography>
              <Chip 
                label={`${totalCost.toFixed(2)} ₽`}
                color="primary"
                size="small"
              />
            </Box>
    
            <Box mb={2}>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                <Box component="span" fontWeight="medium">Цена:</Box> {cost.toFixed(2)} ₽
              </Typography>
              <Typography variant="body2" color="text.secondary" gutterBottom>
                <Box component="span" fontWeight="medium">Количество:</Box> {quantity}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                <Box component="span" fontWeight="medium">За единицу:</Box> {(cost / quantity).toFixed(2)} ₽
              </Typography>
            </Box>
    
            <Box mt="auto">
              <Typography variant="caption" color="text.secondary">
                {formatDate(date)}
              </Typography>
            </Box>
          </CardContent>
    
          <CardActions sx={{ justifyContent: 'space-between', pt: 0, px: 2, pb: 2 }}>
            <Button
              size="small"
              color="primary"
              startIcon={<Edit />}
              onClick={handleEdit}
              variant="outlined"
              fullWidth
              sx={{ mr: 1 }}
            >
              Изменить
            </Button>
            <Button
              size="small"
              color="error"
              startIcon={<Delete />}
              onClick={handleDelete}
              variant="outlined"
              fullWidth
              sx={{ ml: 1 }}
            >
              Удалить
            </Button>
          </CardActions>
        </Card>
      );

}