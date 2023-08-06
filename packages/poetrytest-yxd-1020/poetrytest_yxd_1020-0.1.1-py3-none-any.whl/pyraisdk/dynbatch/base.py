
from abc import ABC, abstractmethod
from typing import Any, List


class BaseModel(ABC):
    '''Base class for models to inherit from
    '''
    
    @abstractmethod
    def predict(self, items: List[Any]) -> List[Any]:
        '''Model predict function
        
        Abstract method which need to be implemented in subclass. It receives
        a bunch of input items, and output same number of predict results.
        
        Args:
            items: Input data items
            
        Returns:
            Predict results for each input data item
        '''
        pass
        
        
    def preprocess(self, items: List[Any]) -> List[Any]:
        '''Preprecossing steps to convert raw data to form consumed by model
        
        Precessing logic is suggested to put in this function. In this way metrics like counting
        and duration will be handled correctly for preprecessong specific. 
        This is not necessary. Default implementation is enought if you just want to
        put every thing in predict function.
        
        Args:
            items: Input data items
            
        Returns:
            Preprocessing results for each input data item
        '''
        return items
    
